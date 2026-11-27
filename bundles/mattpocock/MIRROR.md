# mattpocock skills source ownership and provenance

Fixed acquisition source: https://github.com/mattpocock/skills at
`6f7f7831a625f040a8e06a0e7954826b87ce775a` (MIT, Matt Pocock).
Selected skills from `skills/engineering`: `domain-modeling`,
`grill-with-docs`, `prototype`, `research`, `retro`,
`setup-matt-pocock-skills` and `wayfinder`. Selected from
`skills/productivity`: `grilling` and `writing-for-agents`.
`retro` loads `writing-for-agents` in step 1, and `grill-with-docs` uses
`grilling` and `domain-modeling`. `domain-modeling` follows the upstream
`GLOSSARY.md` convention (work-records #272).
`LICENSE` retains upstream terms and is copied as `LICENSE.txt` in each skill
for standalone native distribution. `UPSTREAM` records the pinned import.

Only adaptation: each `agents/openai.yaml` sidecar is expressed as the Rulesync
`codexcli` frontmatter section, which regenerates the same sidecar for Codex.
Skill bodies are unchanged. No `targets` field, so every selected product
receives every skill.

Consumers explicitly select `bundles/mattpocock` with existing Rulesync
input_roots. Updates re-import a new pinned revision here and reapply through
existing placement; they do not prove native session adoption.

## Checked differences

`python3 tests/check_skills.py` requires every other file under `skills/` to
match the same skill directory upstream, comparing SKILL.md after frontmatter.
Paths are relative to `skills/`:

- license `*/LICENSE.txt`
- omitted `*/agents/openai.yaml`
