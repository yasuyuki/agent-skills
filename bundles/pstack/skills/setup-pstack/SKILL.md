---
targets: [codexcli, claudecode, cursor, antigravity-cli]
name: setup-pstack
description: Configure pstack role models and reasoning budgets through the owning private source and existing Rulesync placement route.
disable-model-invocation: true
---

# Setup pstack

Read [pstack-runtime](../pstack-runtime/SKILL.md). Identify the current harness
from actual tool identity or launch context, then read its matching private
pstack-settings reference and the settings skill's source owner/update route.

Inspect the available native model schema and existing role table/budget. Keep
existing preferences when they already satisfy the request; do not force a new
budget or replace unrelated profiles. A missing role inherits parent explicitly.
Only configure models confirmed available to this harness. An unavailable model
or unknown settings owner is BLOCKED, with the missing prerequisite reported.
Do not silently translate model names. AGY tiers require live measured support.

When the user requests changes, edit only the owning private settings source in
its repository. Record role entries, reasoning budgets and optional panel lists
there. Inherit-parent and auto mean omit the native model override. Panel length
comes from requested/configured independent work, never an upstream fixed count.
Use the existing Rulesync apply/check route from the owner's documentation.
Never write generated profiles, Cursor rules or ~/.agents/pstack-models.md.

Verify source settings, placement and native behavior separately. Report the
owned source changed and any blocked placement/reload/capability check; source
or byte validation alone does not prove a running session adopted settings.
