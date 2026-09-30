# Pstack source ownership and provenance

Fixed acquisition source: https://github.com/backnotprop/pstack at
`157aae39a733135e93d8b5b19ff62c6a84b0ad56` (MIT, Lauren Tan).
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
