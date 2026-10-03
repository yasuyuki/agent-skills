# Evidence and handoff

For a cross-repository audit, keep the result small enough for owners to act on:

1. Scope and observation: triggering change, inspected repository and exact revision, UTC check time, and unavailable sources.
2. Compatibility edges: consumer → provider, purpose (runtime, CI fixture, source, distribution, historical example), current pin/version with file and line, API contract, and evidence status (`verified`, `documented`, `inferred`, or `unknown`). Distinguish a candidate revision from an adopted one.
3. Decision: keep or change each pin, reason, owner, and any condition that would reverse the decision. Do not collapse separate consumers into one global "current version."
4. Ordered owner requests: provider contract and tests; consumer pin/config/docs plus same-commit compatibility test; distribution or environment adoption. Include the exact acceptance command or observable behavior when known, and mark commands needing discovery.
5. Cross-repository gates: source tests, installed-package integration, actual end-to-end entry, evidence of the selected artifact and config, and rollback readiness. State which gates have run and which remain open. Avoid claiming live adoption from examples, CI, or a successful source-only test.

When a documentation version looks stale, trace what its noun refers to and compare the text's original revision with the current owning repository. Classify it as historical context, current pin, test-only fixture, or erroneous current guidance before proposing an edit. Record the confirming source and check date.
