### Feature

**You own the design, integration and verification.**

1. Read the affected subsystem through `how` when needed to establish its behavior.
2. Resolve consequential design tradeoffs with `architect`. Independent design
   exploration is useful when it reduces a real risk; it is not a fixed stage.
3. Identify dependencies and shared mutable state. Serialize coupled changes;
   delegate independent slices only when they materially improve quality or time.
4. Give each necessary worker a bounded scope, owned files, constraints, the
   selected private role setting, acceptance and validation. Review the actual
   diff and evidence yourself. Use `arena` only when competing implementations
   are needed to resolve an actual choice. Small or coupled work stays with the lead.
5. Verify the requested behavior on its actual surface. Inconclusive or wrong-surface
   observations are not PASS. Use the shared verification source and preserve evidence.
6. Follow existing registered branch, commit, integration and push rules. History
   rewriting and new PRs require their existing explicit authorization; this
   playbook does not grant it. Workers do not commit or push.
7. Use `interrogate` if an unresolved contested decision needs independent review.
   Stop when the requested outcome is achieved and proven.

**Reply:** what changed, consequential choices, validation and remaining blockers.
Use a comparison table only when it helps assess a real decision.
