import contextlib
import io
import shutil
import tempfile
import unittest
from pathlib import Path

import check_skills

BUNDLE = check_skills.REPO / "bundles" / "pstack"
# The upstream paragraph agent-skills#8 found merged into an adapted file.
REGAINED = "\nAfter approval, copy the skill folder there and edit the copy. Never open a PR or push.\n"


class RemovedExpressionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.bundle = Path(temporary.name) / "pstack"
        for name in ("MIRROR.md", "REMOVED_EXPRESSIONS.json"):
            (self.bundle / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(BUNDLE / name, self.bundle / name)
        shutil.copytree(BUNDLE / "skills", self.bundle / "skills")
        check_skills.errors.clear()
        self.addCleanup(check_skills.errors.clear)

    def check(self):
        with contextlib.redirect_stderr(io.StringIO()):
            check_skills.check_removed_expressions(self.bundle)
        return check_skills.errors

    def append(self, rel, text):
        with (self.bundle / "skills" / rel).open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(text)

    def test_current_bundle_passes(self):
        self.assertEqual([], self.check())

    def test_regained_upstream_paragraph_in_adapted_file_fails(self):
        self.append("reflect/SKILL.md", REGAINED)
        errors = self.check()
        self.assertEqual(1, len(errors))
        self.assertIn("reflect/SKILL.md:", errors[0])
        self.assertIn("native folder edit", errors[0])

    def test_each_listed_kind_is_detected(self):
        for text in ("Use `claude-opus-5-5-xhigh`.", "Read ~/.claude/rules/pstack-models.md.",
                     "Spawn with `subagent_type: x`.", "Set `readonly: true`.", 'Pass environment: "cloud".'):
            with self.subTest(text=text):
                check_skills.errors.clear()
                self.append("arena/SKILL.md", f"\n{text}\n")
                self.assertEqual(1, len(self.check()))
                shutil.copyfile(BUNDLE / "skills/arena/SKILL.md", self.bundle / "skills/arena/SKILL.md")

    def test_unadapted_upstream_file_is_not_checked(self):
        self.append("tdd/SKILL.md", REGAINED)
        self.assertEqual([], self.check())


if __name__ == "__main__":
    unittest.main()
