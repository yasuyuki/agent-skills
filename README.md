# Agent Skills

Public source for reusable agent skills. Select a skill directory and read its
`SKILL.md`; each directory is standalone and keeps its relative references.
These generic skills are edited here:

- [human-handoff](skills/human-handoff/SKILL.md) — Make remaining human actions reliable to carry out.
- [optimize-human-docs](skills/optimize-human-docs/SKILL.md) — Create or revise human-facing documentation around the reader's decisions and actions.
- [optimize-agent-docs](skills/optimize-agent-docs/SKILL.md) — Create or revise agent instructions while retaining decisions unavailable from code or help.

See [LICENSE](LICENSE) for the MIT license. This repository contains no private
configuration or agent-rules runtime.

## Using the source

Clone this repository at the revision selected by the consumer and give your
agent the path to the selected `skills/<name>/SKILL.md`. Read that file and its
relative references; keep the skill directory intact. An explicit path works
independently of native automatic skill discovery, which depends on the agent
product.

Optional links into an agent's native skills directory are a separate
installation method. Preserve any existing file or directory at the chosen
destination and follow the product's discovery/reload requirements after setup
or update. Updating this source does not prove that a running agent has reloaded
it.

Normal use is simply to read and follow the selected skill. It does not require
regenerating a mirror or selecting an old topic branch before each invocation.

## Project-owned skills

Environment inventory, work classification, and agent-rules verification remain
project-owned in [maintain-environment-inventory](https://github.com/yasuyuki/agent-rules/tree/main/skills/maintain-environment-inventory),
[classify-work](https://github.com/yasuyuki/agent-rules/tree/main/skills/classify-work),
and [verify-agent-rules](https://github.com/yasuyuki/agent-rules/tree/main/skills/verify-agent-rules).
Choose that source explicitly when you need one of those skills; this repository
is not a reverse mirror of it.
