---
targets: [codexcli, claudecode, cursor, antigravity-cli]
name: no-comments
description: "Spawn Comment Sicko, fix accepted findings, and offer encodings for claimed constraints."
disable-model-invocation: true
---

Read [pstack-runtime](../pstack-runtime/SKILL.md) before this workflow. Its native capability, settings, permission and lifecycle contract governs every referenced playbook.


# No comments

Spawn Comment Sicko. Act on accepted findings.

Defer to Comment Sicko's fresh perspective.

## Scope

Use the caller's files or diff. Otherwise use the current diff against the base branch, default `main`, including the working tree.

For a repository-wide review, inventory tracked files with `git ls-files`. Account for Rustdoc and functional comment directives separately from ordinary comments. A directory name alone does not establish that tracked source is generated.

## Steps

1. Delegate a scoped read-only review using pstack-runtime and the prompt in [`references/comment-sicko.md`](references/comment-sicko.md). Apply only authorized changes after the lead reviews findings; unsupported delegation is BLOCKED.
2. Adjudicate findings before applying them. Reject application-code edits, scope escapes, exception-protected deletions, and unsupported `MUST KILL` reasons. Require exact source spans; external-constraint findings must identify the relevant dependency implementation or primary specification. Restating a comment is not proof. Verify that public-API documentation describes an exported contract. Check functional directives and scoped lint or TypeScript suppressions before deleting them. Mark unresolved exceptions `NEEDS REVIEW` and preserve their original text. Investigate thin `IMPORTANT` or `do not remove` claims against the named code and external contract; use `/how` or `/why` when that evidence is insufficient. Rerun a rejected scope once with the failure named. If it is still invalid, leave that scope unchanged and report it unresolved. Continue independently accepted scopes and report partial completion when work remains.
3. Accept a reshape flag only when the current code has a demonstrated defect or missing guarantee. Inspect existing types, tests, and proofs first. A comment explaining correct code, or a possible future edit, does not by itself require rearchitecture. Fix trivial accepted flags directly by deleting a dead path, dropping a parameter, or using the real API. Correctness or safety suppressions remain actionable until their cause is fixed. If an accepted fix needs a shape, run `/architect` once for that set and surrounding code. Stop at the sketch. Step 4 implements.
4. Implement the smallest root-cause fix in scope. Remove every named workaround. If the root cause is out of scope, land the smallest in-scope fix and report the rest open. The **principle-fix-root-causes** and **principle-redesign-from-first-principles** skills guide intent only. Neither authorizes widening the fence nor fixing instances outside it. Never bolt on symptom guards.
5. Constraint comments say `do not remove`, `do not change wording`, or `talk to X before changing`. Preserve proven external constraints. Where an in-scope encoding can replace a necessary comment, offer the cheapest type, runtime check, test, or CI lint and wait for interactive approval. Unattended and eval require caller pre-approval. If approved, encode then delete. Otherwise preserve the comment and report the constraint open. Sketch out-of-scope work separately.
6. Report applied deletions, restored comments, reruns, any architect sketch and fixes, encoding offers and results, and unresolved scopes or constraints. Distinguish accepted work from unadjudicated candidates.
