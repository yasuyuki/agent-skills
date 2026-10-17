---
name: cross-domain-discovery
description: Discover useful, non-obvious methods by matching a problem's causal structure to mechanisms from distant disciplines. Use when familiar approaches constrain the solution space, a stubborn gap remains between current performance and the achievable outcome, or a user asks what approaches they may be overlooking. Complements requirements discovery, research, architecture design, and adversarial review; does not replace them.
---

# Cross-Domain Discovery

Find **transferable mechanisms**, not analogies. Success is a feasible, materially useful approach that the initial solution space lacked. Novelty counts only when it enables a better outcome.

Run on an explicit exploration request, or when an important unresolved gap shows the familiar search space is inadequate. A task with an adequate proven solution gets that solution directly. The output is candidate methods and evidence. It is not implementation, an external change, or permission to widen the user's scope; requirements, safety, privacy, legal limits, and approval boundaries stay as they are.

## Protocol

### 1. Ground the problem

From the user's objective, the authoritative issue/spec, and the evidence already in context (never re-asked), identify:

- **Outcome:** the observable result the user needs and its measure.
- **Non-negotiables:** correctness, safety, operating conditions, permissions, other explicit constraints.
- **Current approach and baseline:** observed results separated from assumptions; unknown stays unknown.
- **Lower bound:** unavoidable work, data, and delay. Legacy steps are not automatically necessary. Record uncertainty when the bound cannot be estimated reliably.
- **Gap:** the dominant causal reasons the outcome is not yet achieved.

Write a short *ordinary baseline*: what a competent agent would recommend from obvious adjacent knowledge. It is the comparison, not an answer to rediscover. Stop here if the objective is met with no important unexplained avoidable burden.

### 2. Remove domain vocabulary

Write 1-3 **mechanism signatures** in causal roles and constraints, free of project nouns and the surface topic:

- What must change, be transported, decided, proven, coordinated, conserved, or observed?
- What makes success hard: information asymmetry, uncertainty, delay, irreversible actions, feedback, combinatorial explosion, conflicting objectives, failure propagation, or another specific mechanism?
- Which quantities, invariants, bottlenecks, and dependencies matter?
- Which current assumptions are implementation choices rather than physical/logical limits?

A signature must discriminate. "We need a more reliable system" is useless; "independent producers make claims that must be traceable to evidence under changing conditions" is usable.

### 3. Search away from the obvious neighborhood

Take at least two routes when the gap warrants it, without forcing unrelated disciplines:

1. **Structural transfer:** fields that already solved the same abstract causal relationship under other names. Search by mechanism and invariant, not the target's vocabulary. Prefer mature, tested methods.
2. **Inversion or regime change:** what method appears if an assumed step is removed, control/data flow is reversed, the resource is treated differently, or the unit of work is redefined? Find fields where that alternative is normal.
3. **Missing capability**, only when routes 1-2 miss a high-impact gap: a field that can audit, measure, recover, or bound something the target cannot.

Draw on mathematical, organizational, natural, legal, scientific, industrial, and safety-engineering fields as the signature suggests; there is no fixed checklist. Use search and source tools when they can change the recommendation: find the **source mechanism** and its operating assumptions before any recipe to copy, prefer primary documentation, standards, scientific work, or field-tested implementations, and reuse trustworthy knowledge already in context when it suffices.

Keep the candidate pool small, discard superficial similarities immediately, and stop expanding when more breadth is unlikely to change the decision. Spawning agents, adding dependencies, and broad web research are off by default.

### 4. Prove the transfer is more than a metaphor

For each promising candidate establish all of:

- **Origin:** the established method or principle borrowed, with a verified source distinguished from a generated hypothesis.
- **Mechanism:** why it works in its own setting, as a causal relationship rather than a shared label.
- **Mapping:** which actors, resources, operations, invariants, and failure modes map from source to target, naming at least one specific correspondence that could be false.
- **Boundary:** which assumptions do not transfer, and which physical, technical, economic, safety, or organizational conditions would invalidate it.
- **Adaptation:** what changes in the target and which existing parts become unnecessary.
- **Discriminator:** the low-cost observation, experiment, prototype, or proof that shows the transfer useful or unsound.

Reject an analogy that cannot explain a causal gain; a prestigious source domain is not evidence of applicability. Label thin-evidence proposals as hypotheses.

### 5. Select for realized benefit

Compare each survivor against the ordinary baseline and the no-change option on:

- Expected improvement in the user-visible outcome (not a proxy or relocated cost).
- Credibility of the causal transfer and strength of evidence.
- Implementation, validation, operating, and human-decision costs.
- Failure risk, reversibility, and consequences of being wrong.
- Whether it removes a structural cause rather than polishing the current process.

Use measured results when available; otherwise state the assumption and uncertainty, never an invented confidence score, optimality bound, or benefit. Recommend **one** candidate; add a distinct runner-up only when it changes the decision. "No distant-domain method passed the gate" is a valid result.

### 6. Return an actionable finding

**Goal / gap:** one or two sentences with baseline and uncertainty.

**Recommended transfer:** `[source discipline: specific method] -> [target operation]`.

**Why non-obvious and useful:** the mechanism, the avoidable burden it removes, and how it differs from the ordinary baseline.

**Applicability and failure boundary:** evidence, key assumptions, invalidating conditions, safety constraints.

**Cheapest decisive check:** a concrete falsifiable test with observable pass/fail and its scope; where it cannot decide alone, the remaining uncertainty.

**Decision:** adopt for detailed design, test first, investigate more, or reject. Unconfirmed outcomes stay marked unconfirmed.

The finding is this shape, not a brainstorm list or a forced discovery. Implementation, issues, and documents follow only on request or when the authorized workflow already needs them.

## Hand-off

Run discovery before choosing an implementation. Optional when those skills are available:

- Ambiguous objective or mapping: Matt Pocock `grill-me` / `grill-with-docs`, or domain-modeling.
- Disputed source-domain fact: Matt Pocock `research`.
- Local architectural friction the discovery points at: Matt Pocock `improve-codebase-architecture`.
- Realizations of a supported transfer: pstack `architect` / `arena`.
- Assumptions, design, and validation of that transfer: pstack `interrogate`.

For delegated work, the Issue remains the execution contract and evidence record.
