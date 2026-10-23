import contextlib
import difflib
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import check_skills


class LocalPatchTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        root = Path(self.temporary.name)
        self.bundle = root / "bundle"
        self.upstream = root / "upstream"
        self.relative = "sample/SKILL.md"
        self.old = "---\nname: sample\n---\n\nOriginal behavior.\n"
        self.new = self.old.replace("Original behavior.", "Preserve unresolved constraints.")
        for directory, text in ((self.upstream, self.old), (self.bundle, self.new)):
            target = directory / "skills" / self.relative
            target.parent.mkdir(parents=True)
            target.write_text(text, encoding="utf-8", newline="\n")
        subprocess.run(["git", "init", "-q", str(self.upstream)], check=True)
        self.patch = self.bundle / "change.patch"
        self.patch.write_text("".join(difflib.unified_diff(
            self.old.splitlines(keepends=True), self.new.splitlines(keepends=True),
            fromfile="a/skills/" + self.relative, tofile="b/skills/" + self.relative,
        )), encoding="utf-8", newline="\n")
        (self.bundle / "LOCAL_PATCHES.json").write_text(json.dumps([{
            "patch": "change.patch", "issue": "https://example.test/upstream/14",
            "files": [self.relative],
        }]), encoding="utf-8")
        check_skills.errors.clear()
        self.addCleanup(check_skills.errors.clear)

    def check(self):
        with contextlib.redirect_stderr(io.StringIO()):
            return check_skills.check_local_patches(self.bundle, self.upstream)

    def test_applied_patch_is_checked_and_exported(self):
        result = self.check()
        self.assertEqual([], check_skills.errors)
        self.assertEqual(check_skills.body(self.new.encode()), result[("sample", "SKILL.md")])

    def test_upstream_refresh_overwriting_local_fix_is_rejected(self):
        (self.bundle / "skills" / self.relative).write_text(self.old, encoding="utf-8", newline="\n")
        self.check()
        self.assertTrue(any("lost or changed" in error for error in check_skills.errors))

    def test_conflicting_upstream_change_is_rejected(self):
        (self.upstream / "skills" / self.relative).write_text(
            self.old.replace("Original behavior.", "Different upstream behavior."),
            encoding="utf-8", newline="\n",
        )
        self.check()
        self.assertTrue(any("cannot apply" in error for error in check_skills.errors))

    def test_native_frontmatter_adaptation_remains_allowed(self):
        source = self.bundle / "skills" / self.relative
        source.write_text(self.new.replace("name: sample", "name: sample\ntargets: [codexcli]"),
                          encoding="utf-8", newline="\n")
        self.check()
        self.assertEqual([], check_skills.errors)


if __name__ == "__main__":
    unittest.main()
