# mattpocock skills source ownership and provenance

Fixed acquisition source: https://github.com/mattpocock/skills at
`49dd158d1076134a641b33efb035946536778336` (MIT, Matt Pocock).
Selected skills: `skills/engineering/retro` and its required
`skills/productivity/writing-for-agents` (retro loads it in step 1).
`LICENSE` retains upstream terms and is copied as `LICENSE.txt` in each skill
for standalone native distribution. `UPSTREAM` records the pinned import.

Only adaptation: each `agents/openai.yaml` sidecar is expressed as the Rulesync
`codexcli` frontmatter section, which regenerates the same sidecar for Codex.
Skill bodies are unchanged. No `targets` field, so every selected product
receives both skills.

Consumers explicitly select `bundles/mattpocock` with existing Rulesync
input_roots. Updates re-import a new pinned revision here and reapply through
existing placement; they do not prove native session adoption.

## Checked differences

`python3 tests/check_skills.py` requires every other file under `skills/` to
match the same skill directory upstream, comparing SKILL.md after frontmatter.
Paths are relative to `skills/`:

- license `*/LICENSE.txt`
- omitted `*/agents/openai.yaml`
