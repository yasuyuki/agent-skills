---
targets: [codexcli, claudecode, cursor, antigravity-cli]
name: pstack-runtime
description: Resolve pstack native harness, private role settings, delegation and workspace boundaries before an operational pstack workflow.
---

# Pstack runtime contract

Common upstream acquired from https://github.com/backnotprop/pstack at
`157aae39a733135e93d8b5b19ff62c6a84b0ad56`; MIT, Lauren Tan. Each standalone
skill retains the fixed upstream notice in `LICENSE.pstack.txt`.

Read this contract before following operational instructions in pstack skills,
references or playbooks. It replaces their vendor parameter examples, fixed
model defaults, extra review counts, permission defaults and lifecycle defaults.
Select only workflow steps, delegation and reports needed to meet or prove the
requested acceptance. Do not add fixed review stages, mandatory fan-out, n/a
throughput checkpoints or principle-compliance reports. Continue authorized
phases without introducing approval gates.

Existing user instructions, trust, authentication, Git/preflight/push policy,
Issue source of truth and workspace ownership always take precedence.

Identify the current harness from native session/product identity or actual tool
schema together with explicit launch context, never from directory presence.
The tool name `Task` alone cannot distinguish Cursor from Claude Code. Supported
native delegation is Cursor `Task`, Claude Code `Agent` or `Task` exactly as
exposed by that session, Codex `collaboration.spawn_agent` with its actual
message/followup/result/interrupt tools, and AGY `invoke_subagent` only when that
tool is actually exposed. Inspect the current tool schema. Do not invent
parameters, registered agent types or APIs. Unsupported delegation, unavailable
configured models or missing required capabilities are **BLOCKED**; report the
specific prerequisite. Do not choose a nearest model or silently execute child
work sequentially in the parent.

For the explicitly identified harness, read only the matching sibling settings
reference: `../pstack-settings/references/cursor.md`, `codex.md`,
`claude-code.md`, or `agy.md`. The private pstack-settings skill supplies source
owner and update route. It is composed by the deployment owner alongside this
public bundle, not distributed here. Deployment must compose pstack-settings as
a sibling through Rulesync; this public source checkout alone is not configured.
Absent role settings mean explicit parent
inheritance: omit native model override. Never restore upstream model defaults.
Use configured panel entries; without them select only independent roles needed
for the requested acceptance, with parent inheritance and no fixed panel count.
Same or inherited models do not establish heterogeneous-model review. Verify
child invocation, result collection and completion from actual native tool/event
metadata. Verify model identity where the native API exposes it; otherwise
record it as unobserved and do not claim model diversity. A child's self-report
or intended prompt alone does not prove execution.
AGY inherit/flash/pro tiers follow the measured native session capability and
private profile, never arbitrary model slug translations.

Preserve existing profile budgets and role preferences when they already solve
the request. Setup changes the owned private source through its documented
route and existing Rulesync apply/check; never edit generated native profiles,
Cursor rules, or ~/.agents/pstack-models.md as a separate writer.

The lead confirms native model availability, chooses necessary independent work,
and owns integration, review of actual diff/evidence, result collection and
termination through actual exposed native APIs. Retrieve results and end or
interrupt children only using the current tool schema and documented native
lifecycle; do not guess a cross-product result or termination mapping. Child prompts must be self-contained, carry the pstack runtime and
verification contract, purpose, explicit host/cwd and owned scope, exclusions,
constraints, acceptance and validation commands. State read-only responsibilities
for designers/reviewers; workers do not commit, push or rewrite Git history.
In Codex, model/reasoning overrides require `fork_turns: "none"` or an explicit
positive history count, never an all-history fork. Give a consolidated prompt
and real accessible source pointers; parent conversation is not portable proof.

Use existing registered worktree, task/Issue, evidence and lifecycle mechanisms.
Do not create unmanaged worktrees, temporary tracking documents, extra PRs or
messaging channels. External writes/messages need existing explicit authority;
autonomy language does not grant permission. Cleanup follows existing ownership,
retention and lifecycle rules, preserves unfinished work/evidence and never
bypasses an approval or isolation boundary. Session/transcript access is limited
to the active authorized workspace; establish ownership from session metadata.
Generated verification skills use project-owned shared source consumable by all
products and the existing placement route, not new native-directory writers.
