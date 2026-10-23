#!/usr/bin/env python3
"""Pre-integration check for skills/ and bundles/*/skills.

1. Rulesync 16.39.1 generates every source root for every consumer target into
   a fresh temporary home, and its own `generate --check` accepts the result.
2. Each bundle with UPSTREAM matches that repository at the pinned commit,
   except the paths listed under "Checked differences" in its MIRROR.md.
   SKILL.md is compared after frontmatter; generated copies are compared too.

Rulesync is RULESYNC_EXECUTABLE or ./node_modules/.bin/rulesync
(`npm ci --ignore-scripts`). Upstream commits are fetched with git.
Missing Rulesync, network or git is a failure.
"""
from __future__ import annotations

import fnmatch
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

VERSION = "16.39.1"
# Union of the targets consumers select; consumers generate skills globally.
TARGETS = ("codexcli", "claudecode", "grokcli", "opencode", "cursor", "antigravity-cli")
REPO = Path(__file__).resolve().parent.parent
ENTRY = re.compile(r"^- (license|added|adapted|omitted) `([^`]+)`$")

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)
    print(f"FAIL: {message}", file=sys.stderr)


def body(data: bytes) -> bytes | None:
    """Bytes after the closing frontmatter delimiter; None without frontmatter."""
    if not data.startswith(b"---\n"):
        return None
    end = data.find(b"\n---\n", 3)
    return None if end < 0 else data[end + 5:]


def content(rel: str, data: bytes) -> bytes | None:
    return body(data) if Path(rel).name == "SKILL.md" else data


def files(root: Path) -> dict[str, Path]:
    return {p.relative_to(root).as_posix(): p for p in sorted(root.rglob("*")) if p.is_file()}


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, check=False, **kwargs)


def rulesync() -> str:
    name = "rulesync.cmd" if os.name == "nt" else "rulesync"
    path = Path(os.environ.get("RULESYNC_EXECUTABLE") or REPO / "node_modules" / ".bin" / name)
    if not path.is_file():
        sys.exit(f"FAIL: Rulesync {VERSION} not found at {path}; run `npm ci --ignore-scripts` or set RULESYNC_EXECUTABLE")
    version = run([str(path), "--version"])
    if version.returncode or version.stdout.strip() != VERSION:
        sys.exit(f"FAIL: {path} is not Rulesync {VERSION}: {(version.stdout + version.stderr).strip()}")
    return str(path)


def generate(executable: str, roots: list[Path], temp: Path) -> dict[str, Path]:
    homes = {}
    for target in TARGETS:
        home = temp / "home" / target
        home.mkdir(parents=True)
        # Global mode writes below HOME; redirect every tool home into the temp tree.
        env = {k: os.environ[k] for k in ("PATH", "SystemRoot", "COMSPEC", "TEMP", "TMP") if k in os.environ}
        env.update({"HOME": str(home), "USERPROFILE": str(home), "XDG_CONFIG_HOME": str(home / ".config"),
                    "XDG_DATA_HOME": str(home / ".local/share"), "CODEX_HOME": str(home / ".codex"),
                    "CLAUDE_CONFIG_DIR": str(home / ".claude"), "GROK_CONFIG_DIR": str(home / ".grok"),
                    "OPENCODE_CONFIG_DIR": str(home / ".config/opencode")})
        base = [executable, "generate", "--targets", target, "--features", "skills", "--global",
                "--input-roots", *map(str, roots)]
        for mode in ("--silent", "--check"):
            result = run([*base, mode], cwd=temp, env=env)
            if result.returncode:
                fail(f"rulesync generate {mode} for {target} exited {result.returncode}: {(result.stderr or result.stdout).strip()}")
                break
        else:
            homes[target] = home
    return homes


def check_generated(skills: dict[str, Path], homes: dict[str, Path], expected) -> None:
    """Every source skill is generated somewhere, each copy matching `expected`."""
    for name, source in skills.items():
        seen = False
        for target, home in homes.items():
            found = list(home.glob(f"**/skills/{name}/SKILL.md"))
            if not found:
                continue
            seen = True
            if len(found) > 1:
                fail(f"{target}: {name} generated more than once")
            out = found[0].parent
            for rel in files(source):
                want = expected(name, rel)
                # Rulesync owns the Codex sidecar path and builds it from frontmatter.
                if want is None or (target == "codexcli" and rel == "agents/openai.yaml"):
                    continue
                path = out / rel
                got = content(rel, path.read_bytes()) if path.is_file() else None
                # Rulesync 16.39.1 drops one blank line right after frontmatter.
                if rel.endswith("SKILL.md") and want.startswith(b"\n"):
                    want = want[1:]
                if got != want:
                    fail(f"{target}: generated {name}/{rel} differs from its expected content")
        if not seen:
            fail(f"{name} was not generated for any target")


def fetch(url: str, commit: str, dest: Path) -> Path:
    steps = [["git", "init", "-q", str(dest)],
             ["git", "-C", str(dest), "fetch", "-q", "--depth", "1", "--no-tags", url, commit],
             ["git", "-C", str(dest), "-c", "core.autocrlf=false", "checkout", "-q", "FETCH_HEAD"]]
    for step in steps:
        result = run(step)
        if result.returncode:
            sys.exit(f"FAIL: cannot fetch {url} at {commit}: {result.stderr.strip()}")
    head = run(["git", "-C", str(dest), "rev-parse", "HEAD"]).stdout.strip()
    if head != commit:
        sys.exit(f"FAIL: {url} resolved to {head}, expected {commit}")
    return dest


def mirror_entries(bundle: Path) -> list[tuple[str, str]]:
    lines = (bundle / "MIRROR.md").read_text(encoding="utf-8").splitlines()
    return [m.groups() for m in map(ENTRY.match, lines) if m]


def check_upstream(bundle: Path, upstream: Path) -> dict[tuple[str, str], bytes]:
    """Compare the bundle with upstream; return expected generated content per (skill, rel)."""
    entries = mirror_entries(bundle)
    used: set[tuple[str, str]] = set()

    def kind(rel: str) -> str | None:
        for entry in entries:
            if fnmatch.fnmatchcase(rel, entry[1]):
                used.add(entry)
                return entry[0]
        return None

    license_bytes = (bundle / "LICENSE").read_bytes()
    if license_bytes != (upstream / "LICENSE").read_bytes():
        fail(f"{bundle.name}/LICENSE differs from upstream LICENSE")
    upstream_dirs: dict[str, list[Path]] = {}
    for skill in upstream.rglob("SKILL.md"):
        upstream_dirs.setdefault(skill.parent.name, []).append(skill.parent)
    expected = {}
    for source in sorted(p for p in (bundle / "skills").iterdir() if p.is_dir()):
        name = source.name
        candidates = upstream_dirs.get(name, [])
        if len(candidates) > 1:
            fail(f"{bundle.name}: upstream has several {name} skill directories")
        ours = files(source)
        theirs = files(candidates[0]) if len(candidates) == 1 else {}
        for rel in sorted(ours.keys() | theirs.keys()):
            path, label = f"{name}/{rel}", f"{bundle.name}/skills/{name}/{rel}"
            how = kind(path)
            if rel not in ours:
                if how != "omitted":
                    fail(f"{label} exists upstream but is missing")
                continue
            data = ours[rel].read_bytes()
            mine = content(rel, data)
            if mine is None:
                fail(f"{label} has no closing frontmatter")
                continue
            if rel.endswith("SKILL.md") and not mine.strip():
                fail(f"{label} has an empty body")
            if how == "license":
                if data != license_bytes:
                    fail(f"{label} differs from {bundle.name}/LICENSE")
            elif rel not in theirs:
                if how != "added":
                    fail(f"{label} has no upstream counterpart and is not listed in MIRROR.md")
            elif how != "adapted":
                upstream_content = content(rel, theirs[rel].read_bytes())
                if mine != upstream_content:
                    fail(f"{label} differs from upstream" + (" after frontmatter" if rel.endswith("SKILL.md") else ""))
                expected[(name, rel)] = upstream_content
    for entry in entries:
        if entry not in used:
            fail(f"{bundle.name}/MIRROR.md entry {entry[0]} `{entry[1]}` matches no file")
    return expected


def check_local_patches(bundle: Path, upstream: Path) -> dict[tuple[str, str], bytes]:
    manifest = bundle / "LOCAL_PATCHES.json"
    if not manifest.is_file():
        return {}
    expected = {}
    for entry in json.loads(manifest.read_text(encoding="utf-8")):
        patch = bundle / entry["patch"]
        issue = entry["issue"]
        for mode in (("--check",), ()):
            result = run(["git", "-C", str(upstream), "apply", *mode, str(patch.resolve())])
            if result.returncode:
                fail(f"{bundle.name}: temporary patch {entry['patch']} cannot apply; reconcile {issue}: {result.stderr.strip()}")
                break
        else:
            for rel in entry["files"]:
                name, resource = rel.split("/", 1)
                source = bundle / "skills" / rel
                patched = upstream / "skills" / rel
                want = content(resource, patched.read_bytes())
                if content(resource, source.read_bytes()) != want:
                    fail(f"{bundle.name}: {rel} lost or changed its temporary patch; reconcile {issue}")
                expected[(name, resource)] = want
    return expected


def main() -> int:
    roots = [REPO, *sorted(p.parent for p in (REPO / "bundles").glob("*/skills") if p.is_dir())]
    skills: dict[str, Path] = {}
    for root in roots:
        for source in sorted(p for p in (root / "skills").iterdir() if p.is_dir()):
            if source.name in skills:
                fail(f"skill {source.name} exists in more than one source root")
            skills[source.name] = source
            if not (source / "SKILL.md").is_file():
                fail(f"{source.relative_to(REPO)} has no SKILL.md")
    executable = rulesync()
    with tempfile.TemporaryDirectory(prefix="check-skills-") as temp_name:
        temp = Path(temp_name)
        upstream_expected: dict[tuple[str, str], bytes] = {}
        for root in roots[1:]:
            if not (root / "UPSTREAM").is_file():
                continue
            url, commit = (root / "UPSTREAM").read_text(encoding="utf-8").split()[:2]
            upstream = fetch(url, commit, temp / "upstream" / root.name)
            upstream_expected.update(check_upstream(root, upstream))
            upstream_expected.update(check_local_patches(root, upstream))
        homes = generate(executable, roots, temp)

        def expected(name: str, rel: str) -> bytes | None:
            if (name, rel) in upstream_expected:
                return upstream_expected[(name, rel)]
            return content(rel, (skills[name] / rel).read_bytes())

        if len(homes) == len(TARGETS):
            check_generated(skills, homes, expected)
    if errors:
        print(f"{len(errors)} check failure(s)", file=sys.stderr)
        return 1
    print(f"OK: {len(skills)} skills from {len(roots)} roots generated for {len(TARGETS)} targets; upstream bodies match")
    return 0


if __name__ == "__main__":
    sys.exit(main())
