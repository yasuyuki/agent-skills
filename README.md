# Agent Skills

Generated public mirror of the original skills maintained in
[agent-rules](https://github.com/yasuyuki/agent-rules). **Edit skills upstream in
agent-rules; do not edit this repository’s generated `skills/` subtree.**
Each skill has a `SKILL.md` with name and description metadata, plus any referenced
files. This checkout can be read by an agent supporting that format.

## Published skills

- **human-handoff** — Make remaining human actions reliable to carry out.
- **maintain-environment-inventory** — Maintain environment references and management
  skill placement when changing or selecting a runtime.
- **classify-work** — Classify unfinished work and propose suitable environments
  without executing the work.
- **verify-agent-rules** — Exercise placement and safe updates with disposable data
  and retained evidence; optionally verify dependency composition and mirroring.

Publication is original-work-only. The upstream `skills/UPSTREAM.tsv` controls
exclusion: `grilling` and `create-verification-skill` are intentionally absent.
This mirror does not contain all upstream skills, the agent-rules CLI, or private
configuration. See [LICENSE](LICENSE) for the MIT license.

## Using the public mirror

For initial setup, clone this repository’s `main` branch and give your agent the
path to the selected `skills/<name>/SKILL.md`. Read that file and its relative
references; keep the skill directory intact. An explicit path works independently
of native automatic skill discovery, which depends on the agent product.

For example, ask the agent to read `skills/verify-agent-rules/SKILL.md` from this
checkout and verify a selected agent-rules checkout. It runs **this distributed
skill’s** `scripts/verify.py` by its actual path, with the target checkout supplied
through `--repo`. Python 3.10+ and Git are required. The default profile needs no
private repository and prints the path to retained verification evidence.

Optional links into an agent’s native skills directory are a separate installation
method from managed placement. Preserve any existing file or directory at the
chosen destination. Follow the product’s discovery/reload requirements after
setup or update. Updating this checkout changes linked files, but does not prove
that a running agent has reloaded them or that other environments adopted them.
Existing link users do not need to migrate for this publication repair.

Normal use is simply to read and follow the selected skill. It does not require
regenerating this mirror, checking synchronization, selecting an old topic branch,
or auditing adoption history before each invocation.

## Managed environments

Use the environment’s existing declaration and the upstream agent-rules
`place.py apply` / `check` entry points to place and compare skills from the
canonical source. Do not add this mirror as a second source for the same skills.
Environments needing excluded skills continue to use that upstream placement
path. Updating this public checkout does not update managed environments.

## Updating the publication

Maintainers first integrate skill changes in agent-rules and select that committed
source. Use the existing public `bin/place.py mirror` command from that source;
`mirror --help` describes `--skills`, `--dest`, and `--check`. The source argument
selects its `skills/` directory and the destination is the protected agent-skills
candidate checkout. No private configuration is required.

The generator owns the entire destination `skills/` subtree, including removal of
unexpected content. Inspect local changes and use a disposable output before
applying it to a candidate. Preserve unrelated root files such as this README and
LICENSE, and keep unmanaged or unsaved content outside the generated subtree.
Run the same command with `--check`, compare the manifest-selected file set,
bytes and required executable attributes, and verify repeat generation and drift
detection in disposable output. Update this skill list when the public set changes.

Review and commit the generated output with the selected upstream revision in the
commit message, then use the repository’s normal integration route to `main`.
That commit records provenance; there is no separate source ledger. Consumers
update their checkout from `main` through their existing Git workflow and follow
any product-specific reload steps. Generation is an upstream-change operation,
not a prerequisite for ordinary skill use.
