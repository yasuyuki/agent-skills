#!/usr/bin/env python3
"""Import a new upstream revision into an adapted bundle.

    python3 tools/import_upstream.py bundles/pstack <new-commit>

Reads the bundle's UPSTREAM, fetches the pinned and the new commit, and applies
the upstream change under skills/ to the bundle:

- an unchanged file takes the upstream bytes; an adapted file is merged three
  ways (adapted, pinned upstream, new upstream);
- a new skill directory gets the bundle's `targets:` frontmatter line and its
  license copy; upstream LICENSE changes reach every license copy;
- a file upstream deleted is removed unless the bundle changed it;
- the pinned SHA is replaced in UPSTREAM, MIRROR.md and the bundle's own files;
- upstream's executable bit is set, and also staged when the bundle is in a
  Git checkout, because Windows checkouts ignore file modes;
- a LOCAL_PATCHES.json patch that no longer applies is rewritten against
  the new upstream.

A conflict leaves merge markers in that file; a deleted adapted file is kept.
Both are listed, with new skills and the adapted files to review, and the exit
status is 1. Resolve them per the bundle's MIRROR.md, then run
tests/check_skills.py.
"""
from __future__ import annotations

import collections
import difflib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SHA = re.compile(r"^[0-9a-f]{40}$")


def git(*args: str, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True)
    if check and result.returncode:
        sys.exit(f"git {' '.join(args)} failed: {result.stderr.decode(errors='replace').strip()}")
    return result


def frontmatter_end(data: bytes) -> int | None:
    if not data.startswith(b"---\n"):
        return None
    end = data.find(b"\n---\n", 3)
    return None if end < 0 else end + 5


def with_targets(data: bytes, line: bytes) -> bytes:
    if frontmatter_end(data) is None or data.startswith(b"---\n" + line):
        return data
    return b"---\n" + line + data[4:]


def adapted_content(rel: str, ours: bytes, upstream: bytes) -> bytes:
    """What a local patch must turn the upstream file into (check_skills compares SKILL.md bodies)."""
    if Path(rel).name != "SKILL.md":
        return ours
    up_end, our_end = frontmatter_end(upstream), frontmatter_end(ours)
    if up_end is None or our_end is None:
        return ours
    return upstream[:up_end] + ours[our_end:]


def unified(rel: str, before: bytes, after: bytes) -> str:
    lines = difflib.unified_diff(before.decode().splitlines(keepends=True), after.decode().splitlines(keepends=True),
                                 fromfile=f"a/skills/{rel}", tofile=f"b/skills/{rel}")
    # git apply accepts an empty line as blank context; a lone space trips `git diff --check`.
    return "".join("\n" if line == " \n" else line for line in lines)


class Import:
    def __init__(self, bundle: Path, upstream: Path, old: str, new: str):
        self.bundle, self.upstream, self.old, self.new = bundle, upstream, old, new
        self.skills = bundle / "skills"
        self.conflicts: list[str] = []
        self.kept: list[str] = []
        self.merged: list[str] = []
        self.new_skills: list[str] = []
        self.removed_skills: list[str] = []
        self.counts = collections.Counter()

    def blob(self, commit: str, path: str) -> bytes:
        return git("show", f"{commit}:{path}", cwd=self.upstream).stdout

    def targets_line(self) -> bytes:
        lines = collections.Counter()
        for skill in self.skills.glob("*/SKILL.md"):
            first = skill.read_bytes().split(b"\n", 2)
            if len(first) > 1 and first[1].startswith(b"targets:"):
                lines[first[1] + b"\n"] += 1
        return lines.most_common(1)[0][0] if lines else b""

    def license_name(self) -> str | None:
        mirror = (self.bundle / "MIRROR.md").read_text(encoding="utf-8")
        found = re.search(r"^- license `\*/([^`/]+)`$", mirror, re.M)
        return found.group(1) if found else None

    def merge(self, rel: str, ours: bytes, base: bytes, theirs: bytes, line: bytes = b"") -> None:
        with tempfile.TemporaryDirectory() as temp:
            paths = []
            for name, data in (("ours", ours), ("base", base), ("theirs", theirs)):
                path = Path(temp) / name
                path.write_bytes(data)
                paths.append(str(path))
            result = git("merge-file", "-p", "-L", "adapted", "-L", f"upstream {self.old[:8]}",
                         "-L", f"upstream {self.new[:8]}", *paths, check=False)
        if result.returncode < 0 or result.returncode > 127:
            self.kept.append(f"{rel} (cannot merge; adapted bytes kept)")
            return
        (self.skills / rel).write_bytes(with_targets(result.stdout, line) if line else result.stdout)
        (self.conflicts if result.returncode else self.merged).append(rel)

    def apply_skills(self) -> None:
        listing = git("diff", "--no-renames", "--name-status", "-z", self.old, self.new, "--", "skills",
                      cwd=self.upstream).stdout.decode().split("\0")
        existing = {p.name for p in self.skills.iterdir() if p.is_dir()}
        targets = self.targets_line()
        for status, path in zip(listing[::2], listing[1::2]):
            rel = path.removeprefix("skills/")
            target = self.skills / rel
            ours = target.read_bytes() if target.is_file() else None
            # The native `targets:` line is ours; compare and merge without it, then restore it.
            line = b""
            if ours is not None and targets and ours.startswith(b"---\n" + targets):
                line, ours = targets, b"---\n" + ours[4 + len(targets):]
            if status == "A":
                theirs = self.blob(self.new, path)
                if ours is None or ours == theirs:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(theirs)
                    self.counts["added"] += 1
                else:
                    self.merge(rel, ours, b"", theirs)
                if rel.split("/")[0] not in existing and rel.split("/")[0] not in self.new_skills:
                    self.new_skills.append(rel.split("/")[0])
                continue
            base = self.blob(self.old, path)
            if status == "D":
                if ours is None:
                    continue
                if ours == base:
                    target.unlink()
                    self.counts["deleted"] += 1
                else:
                    self.kept.append(f"{rel} (deleted upstream, adapted here)")
                continue
            theirs = self.blob(self.new, path)
            if ours is None:
                self.kept.append(f"{rel} (changed upstream, absent here)")
            elif ours == base:
                target.write_bytes(with_targets(theirs, line) if line else theirs)
                self.counts["updated"] += 1
            else:
                self.merge(rel, ours, base, theirs, line)
        self.mark_executables({p.removeprefix("skills/") for p in listing[1::2]})

    def mark_executables(self, changed: set[str]) -> None:
        """Carry upstream's executable bit, in the index too where Git ignores file modes."""
        tree = git("ls-tree", "-r", "-z", self.new, "--", "skills", cwd=self.upstream).stdout.decode()
        executables = []
        for entry in filter(None, tree.split("\0")):
            meta, path = entry.split("\t", 1)
            rel = path.removeprefix("skills/")
            if meta.startswith("100755") and rel in changed and (self.skills / rel).is_file():
                (self.skills / rel).chmod(0o755)
                executables.append(str(self.skills / rel))
        inside = git("rev-parse", "--is-inside-work-tree", cwd=self.skills, check=False)
        if executables and not inside.returncode:
            git("add", "--chmod=+x", "--", *executables, cwd=self.skills)

    def finish_skill_dirs(self) -> None:
        line, license_name = self.targets_line(), self.license_name()
        notice = (self.bundle / "LICENSE").read_bytes()
        for name in self.new_skills:
            skill = self.skills / name / "SKILL.md"
            if skill.is_file():
                skill.write_bytes(with_targets(skill.read_bytes(), line))
            if license_name:
                (self.skills / name / license_name).write_bytes(notice)
        for directory in sorted(p for p in self.skills.iterdir() if p.is_dir()):
            left = [p for p in directory.rglob("*") if p.is_file() and p.name != license_name]
            if not left:
                for path in sorted(directory.rglob("*"), key=lambda p: len(p.parts), reverse=True):
                    path.unlink() if path.is_file() else path.rmdir()
                directory.rmdir()
                self.removed_skills.append(directory.name)
            else:
                for empty in sorted((p for p in directory.rglob("*") if p.is_dir()), key=lambda p: len(p.parts),
                                    reverse=True):
                    if not any(empty.iterdir()):
                        empty.rmdir()

    def update_license(self) -> None:
        theirs = self.blob(self.new, "LICENSE")
        if theirs == (self.bundle / "LICENSE").read_bytes():
            return
        (self.bundle / "LICENSE").write_bytes(theirs)
        name = self.license_name()
        for copy in self.skills.glob(f"*/{name}") if name else ():
            copy.write_bytes(theirs)
        self.counts["license copies"] += 1

    def replace_pin(self) -> None:
        old, new = self.old.encode(), self.new.encode()
        for path in sorted(p for p in self.bundle.rglob("*") if p.is_file()):
            data = path.read_bytes()
            if old in data:
                path.write_bytes(data.replace(old, new))
                self.counts["pin references"] += 1

    def rewrite_local_patches(self) -> None:
        manifest = self.bundle / "LOCAL_PATCHES.json"
        if not manifest.is_file():
            return
        for entry in json.loads(manifest.read_text(encoding="utf-8")):
            if any(rel in self.conflicts for rel in entry["files"]):
                self.kept.append(f"{entry['patch']} (not rewritten; resolve its files, then rerun or edit)")
                continue
            patch = self.bundle / entry["patch"]
            wanted = {rel: adapted_content(rel, (self.skills / rel).read_bytes(), self.blob(self.new, f"skills/{rel}"))
                      for rel in entry["files"]}
            if self.still_applies(patch, wanted):
                continue
            text = "".join(unified(rel, self.blob(self.new, f"skills/{rel}"), data) for rel, data in wanted.items())
            patch.write_bytes(text.encode())
            self.counts["rewritten patches"] += 1
            if not text:
                self.kept.append(f"{entry['patch']} (now empty: upstream covers it; retire it per MIRROR.md)")

    def still_applies(self, patch: Path, wanted: dict[str, bytes]) -> bool:
        """The existing patch applies to the new upstream and yields the adapted content."""
        try:
            if git("apply", str(patch.resolve()), cwd=self.upstream, check=False).returncode:
                return False
            return all((self.upstream / "skills" / rel).read_bytes() == data for rel, data in wanted.items())
        finally:
            git("checkout", "-q", "--", ".", cwd=self.upstream)

    def report(self) -> int:
        counts = ", ".join(f"{n} {k}" for k, n in sorted(self.counts.items()))
        print(f"Imported {self.old[:8]}..{self.new[:8]}: {counts or 'no direct file updates'}")
        sections = [("Conflicts (merge markers left)", self.conflicts),
                    ("Kept for decision", self.kept),
                    ("New skills (review adaptation and MIRROR.md entries)", self.new_skills),
                    ("Removed skills (remove their MIRROR.md entries)", self.removed_skills),
                    ("Adapted files merged cleanly (review the upstream hunks)", self.merged)]
        for title, items in sections:
            if items:
                print(f"{title}:")
                print("".join(f"  {item}\n" for item in items), end="")
        print("Next: resolve per MIRROR.md 'Updating upstream', then python3 tests/check_skills.py")
        return 1 if self.conflicts or self.kept or self.new_skills or self.removed_skills else 0


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    bundle, wanted = Path(argv[0]).resolve(), argv[1]
    url, old = (bundle / "UPSTREAM").read_text(encoding="utf-8").split()[:2]
    with tempfile.TemporaryDirectory(prefix="import-upstream-") as temp:
        upstream = Path(temp)
        git("init", "-q", str(upstream))
        git("config", "core.autocrlf", "false", cwd=upstream)
        git("fetch", "-q", "--depth", "1", "--no-tags", url, old, cwd=upstream)
        git("fetch", "-q", "--depth", "1", "--no-tags", url, wanted, cwd=upstream)
        new = git("rev-parse", "FETCH_HEAD", cwd=upstream).stdout.decode().strip()
        git("checkout", "-q", "--detach", new, cwd=upstream)
        if not SHA.match(old) or not SHA.match(new):
            sys.exit(f"UPSTREAM pin {old} or new commit {new} is not a full SHA")
        if new == old:
            print(f"Already at {new}")
            return 0
        run = Import(bundle, upstream, old, new)
        run.apply_skills()
        run.update_license()
        run.finish_skill_dirs()
        run.replace_pin()
        run.rewrite_local_patches()
        return run.report()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
