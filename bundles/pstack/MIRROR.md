# Pstack source ownership and provenance

Fixed acquisition source: https://github.com/backnotprop/pstack at
`6c75f4e67546c2ddbf9634734c1e3ebbea34861a` (MIT, Lauren Tan).
This is one adapted copy; support references, playbooks and scripts are retained.
`LICENSE` retains upstream terms. Its fixed notice is copied as
`LICENSE.pstack.txt` in each skill for standalone native distribution. `UPSTREAM` records the pinned import.

Rulesync source frontmatter selects only codexcli, claudecode, cursor and
antigravity-cli through its native targets field. Generation strips that field
from native skill frontmatter; existing other-product sources remain selected.

Deliberate adaptations: directory IDs are frontmatter names; poteto-mode permits
model invocation; native capability/settings/permission/lifecycle resolution is
shared in pstack-runtime; setup updates private owned settings via Rulesync;
unconfigured roles inherit parent rather than fixed upstream model slugs.
Feature/investigation paths omit routine n/a checkpoints, forced delegation and
unrequested history/PR operations under the runtime acceptance contract.
The custom create-verification-skill is primary, imported from agent-rules
`skills/create-verification-skill` at `bb93bfcffd117dc7c628052e8939e8320084b609`. Its LICENSE.txt and sources
reference retain its provenance; upstream feature-map support remains available.
Generated verification source is project-owned and shared across products.

Consumers explicitly select `bundles/pstack` with existing Rulesync input_roots.
Generic `skills/` selection remains unchanged. Private settings are independently
owned and composed through a separate input root. The common bundle owner makes
one revision/adaptation decision here, validates it and reapplies via existing
placement; product adapters do not fork or independently rewrite this source.
Updates do not prove native session adoption; behavioral acceptance belongs to
the deployment owner. No installer or launch wrapper is added.

## Updating upstream

Run `python3 tools/import_upstream.py bundles/pstack <commit>` from the
repository root in a task checkout. It merges the change since `UPSTREAM`,
prepares new skills, repins and rewrites a local patch that no longer applies.
It exits 1 with what remains:

- **Conflicts.** Keep the adapted side wherever it routes through
  pstack-runtime or the private profile: delegation, models, settings,
  permissions and lifecycle. Take upstream wording and behavior elsewhere.
  When upstream rewrites an adapted workflow, start from its new body and
  re-apply the same adaptation.
- **Deleted adapted files.** Delete them with their adapted entries when
  upstream removed the feature. Keep one only for a behavior the adaptation
  still needs, and say why in the commit.
- **New skills.** A workflow that delegates, picks models or edits settings
  gets the pstack-runtime line and an adapted entry. Others stay upstream.
- **Removed skills.** Remove their entries below.
- **Adapted files merged cleanly.** Read their upstream hunks.
  `tests/check_skills.py` rejects the expressions in `REMOVED_EXPRESSIONS.json`,
  not every conflict with the runtime contract.

Then run the unit tests and `tests/check_skills.py`.

## Temporary no-comments patch

[pstack #14](https://github.com/backnotprop/pstack/issues/14) tracks the
evidence and scope-isolation problem observed in a downstream comment review.
`LOCAL_PATCHES.json` records the patch against the selected `UPSTREAM` revision.
The source check applies it to a disposable upstream checkout and compares the
result with the distributed sources. An overwritten adaptation or a conflicting
upstream update fails that check.

The checked patch includes the existing native-delegation adaptation so the
comparison covers the complete downstream body. Keep that runtime contract when
retiring the temporary review changes.

Upstream closed #14 in `02b59d7`, keeping unverifiable outside-rule comments
under `REVIEW` and continuing after a rejected rerun. The patch already covers
both and still adds the repository-wide inventory, primary-source citations and
per-scope partial completion, so it is rebased onto the selected revision.
Remove it when upstream covers that remaining difference and its behavior is
verified, with the decision recorded in the owning task. Update the patch,
manifest, and adapted-path entries together.

## Windows statechart patch

`patches/statechart-windows.patch` lets statechart run on Windows
([agent-skills#14](https://github.com/yasuyuki/agent-skills/issues/14)). It
replaces the `/bin/sh` cleanup with `taskkill` and a runtime-evaluated janitor,
points the worker's `TEMP` and `TMP` at the folder that cleanup removes, and
splits TLC output on CRLF, which TLC writes after each message on Windows.
POSIX keeps the upstream commands. Remove the patch when upstream runs on
Windows.

## Checked differences

`python3 tests/check_skills.py` requires every other file under `skills/` to
match the same skill directory upstream, comparing SKILL.md after frontmatter.
It also fails when an adapted file contains a pattern from
`REMOVED_EXPRESSIONS.json`: upstream model slugs, settings paths, vendor
parameters and native skill folder edits that the adaptation removed. A clean
three-way merge can restore them silently. Upstream-verbatim files are not
checked. Add a pattern there when an adaptation removes a new kind of expression.
Paths are relative to `skills/`:

- license `*/LICENSE.pstack.txt`
- license `create-verification-skill/LICENSE.txt`
- added `pstack-runtime/SKILL.md`
- added `create-verification-skill/references/sources.md`
- adapted `architect/SKILL.md`
- adapted `arena/SKILL.md`
- adapted `automate-me/SKILL.md`
- adapted `create-formal-verification-skill/SKILL.md`
- adapted `create-verification-skill/SKILL.md`
- adapted `figure-it-out/SKILL.md`
- adapted `how/SKILL.md`
- adapted `interrogate/SKILL.md`
- adapted `maintain-verification-skill/SKILL.md`
- adapted `maintain-formal-verification-skill/SKILL.md`
- adapted `make-bot-ui/SKILL.md`
- adapted `no-comments/SKILL.md`
- adapted `no-comments/references/comment-sicko.md`
- adapted `poteto-help/SKILL.md`
- adapted `poteto-mode/SKILL.md`
- adapted `poteto-mode/playbooks/bug-fix.md`
- adapted `poteto-mode/playbooks/feature.md`
- adapted `poteto-mode/playbooks/hillclimb.md`
- adapted `poteto-mode/playbooks/investigation.md`
- adapted `poteto-mode/playbooks/multi-phase-plan.md`
- adapted `poteto-mode/playbooks/perf-issue.md`
- adapted `poteto-mode/playbooks/refactoring.md`
- adapted `poteto-mode/playbooks/shipping.md`
- adapted `poteto-mode/playbooks/runtime-forensics.md`
- adapted `poteto-mode/playbooks/trace-forensics.md`
- adapted `principle-never-block-on-the-human/SKILL.md`
- adapted `recall/SKILL.md`
- adapted `reflect/SKILL.md`
- adapted `setup-pstack/SKILL.md`
- adapted `show-me-your-work/SKILL.md`
- adapted `statechart/scripts/frontends/dot.ts`
- adapted `statechart/scripts/run.ts`
- adapted `statechart/scripts/statechart.ts`
- adapted `swarm/SKILL.md`
- adapted `why/SKILL.md`
