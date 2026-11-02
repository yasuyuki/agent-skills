import contextlib
import io
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import import_upstream  # noqa: E402

TARGETS = "targets: [codexcli, claudecode]\n"


def skill(name, body):
    return f"---\nname: {name}\ndescription: {name} skill\n---\n\n{body}\n"


class ImportUpstreamTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        self.upstream, self.bundle = root / "upstream", root / "bundle"
        self.git("init", "-q", str(self.upstream))
        self.git("config", "core.autocrlf", "false", cwd=self.upstream)
        self.old = self.commit({
            "LICENSE": "MIT\n",
            "skills/one/SKILL.md": skill("one", "First.\n\nSecond.\n\nThird."),
            "skills/two/SKILL.md": skill("two", "Plain."),
            "skills/gone/SKILL.md": skill("gone", "Going."),
        })
        self.write(self.bundle, {
            "UPSTREAM": f"{self.upstream.as_posix()}\n{self.old}\n",
            "LICENSE": "MIT\n",
            "MIRROR.md": f"Pinned at `{self.old}`.\n\n- license `*/LICENSE.up.txt`\n- adapted `one/SKILL.md`\n",
            "skills/one/SKILL.md": "---\n" + TARGETS + skill("one", "First, adapted.\n\nSecond.\n\nThird.")[4:],
            "skills/two/SKILL.md": "---\n" + TARGETS + skill("two", "Plain.")[4:],
            "skills/gone/SKILL.md": "---\n" + TARGETS + skill("gone", "Going.")[4:],
            "skills/runtime/SKILL.md": "---\n" + TARGETS + skill("runtime", f"Acquired at `{self.old}`.")[4:],
            **{f"skills/{n}/LICENSE.up.txt": "MIT\n" for n in ("one", "two", "gone", "runtime")},
        })

    def git(self, *args, cwd=None):
        return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()

    @staticmethod
    def write(root, files):
        for rel, text in files.items():
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(text.encode())

    def commit(self, files, delete=(), executable=()):
        self.write(self.upstream, files)
        for rel in delete:
            self.git("rm", "-q", rel, cwd=self.upstream)
        self.git("add", "-A", cwd=self.upstream)
        for rel in executable:
            self.git("update-index", "--chmod=+x", rel, cwd=self.upstream)
        self.git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "c", cwd=self.upstream)
        return self.git("rev-parse", "HEAD", cwd=self.upstream)

    def run_import(self, commit):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            status = import_upstream.main([str(self.bundle), commit])
        return status, out.getvalue()

    def read(self, rel):
        return (self.bundle / rel).read_bytes().decode()

    def test_update_merges_adds_deletes_and_repins(self):
        new = self.commit({
            "skills/one/SKILL.md": skill("one", "First.\n\nSecond.\n\nThird, upstream."),
            "skills/two/SKILL.md": skill("two", "Plain, upstream."),
            "skills/three/SKILL.md": skill("three", "New."),
            "skills/three/run": "#!/bin/sh\n",
        }, delete=["skills/gone/SKILL.md"], executable=["skills/three/run"])
        status, out = self.run_import(new)
        self.assertEqual(1, status, out)  # the new skill needs review
        self.assertIn("three", out)
        self.assertEqual("---\n" + TARGETS + skill("one", "First, adapted.\n\nSecond.\n\nThird, upstream.")[4:],
                         self.read("skills/one/SKILL.md"))
        self.assertEqual("---\n" + TARGETS + skill("two", "Plain, upstream.")[4:], self.read("skills/two/SKILL.md"))
        self.assertTrue(self.read("skills/three/SKILL.md").startswith("---\n" + TARGETS))
        self.assertEqual("MIT\n", self.read("skills/three/LICENSE.up.txt"))
        self.assertFalse((self.bundle / "skills/gone").exists())
        for rel in ("UPSTREAM", "MIRROR.md", "skills/runtime/SKILL.md"):
            self.assertIn(new, self.read(rel))
            self.assertNotIn(self.old, self.read(rel))
        if os.name != "nt":
            self.assertTrue(os.access(self.bundle / "skills/three/run", os.X_OK))

    def test_conflicting_adapted_line_keeps_markers_and_fails(self):
        new = self.commit({"skills/one/SKILL.md": skill("one", "First, upstream.\n\nSecond.\n\nThird.")})
        status, out = self.run_import(new)
        self.assertEqual(1, status)
        self.assertIn("one/SKILL.md", out)
        text = self.read("skills/one/SKILL.md")
        self.assertIn("<<<<<<< adapted", text)
        self.assertTrue(text.startswith("---\n" + TARGETS))

    def test_unadapted_update_succeeds(self):
        new = self.commit({"skills/two/SKILL.md": skill("two", "Plain, upstream.")})
        status, out = self.run_import(new)
        self.assertEqual(0, status, out)
        self.assertIn(new, self.read("UPSTREAM"))


if __name__ == "__main__":
    unittest.main()
