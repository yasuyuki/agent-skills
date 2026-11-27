# anthropic skills source ownership and provenance

Fixed acquisition source: https://github.com/anthropics/skills at
`e4bb5d960d87126ff3b3a8af1a104b7db67560ba` (Apache-2.0, Anthropic).
Selected skill: `skills/frontend-design`, copied unchanged with its own
`LICENSE.txt` (work-records #272).

Upstream has no repository-level `LICENSE`, so this bundle has no `UPSTREAM`
file and `tests/check_skills.py` checks it as an owned source, not against
upstream. Update it by copying `skills/frontend-design` from a new pinned
revision and changing the revision above.

Consumers explicitly select `bundles/anthropic` with existing Rulesync
input_roots. Updates reapply through existing placement; they do not prove
native session adoption.
