---
name: coordinate-repository-versions
description: Coordinate version and pin changes across related repositories when an API, runtime, test fixture, or deployment contract may be affected. Use for cross-repo compatibility audits and migration plans, not routine single-repo dependency updates.
---

# Coordinate repository versions

Establish a compatible, adoptable set of revisions for the requested change. A newer package version is not, by itself, a reason to replace a fixed revision. Keep each repository's implementation, consumer configuration, tests, and documentation with their respective owners.

## Scope the inquiry

Start with the changed behavior and its directly affected producer and consumer. Identify other repositories only when imports, CLI calls, generated artifacts, pins, or deployment paths lead to them. Search relevant manifests, lockfiles, CI, code, tests, configuration examples, and current owner docs; expand only where a discovered edge requires it. Record the inspected revision and UTC observation time; if a source exposes only a floating branch, mark its exact revision unknown. Treat historical examples, test fixtures, runtime pins, and live configuration as different evidence classes. A public example does not establish the private deployed value.

For each edge, record **consumer → provider**, owner, purpose, observed revision/version and source location, required API or file contract, and evidence strength. Confirm a claimed version against the referenced commit or installed artifact where accessible. Mark missing repositories, private pins, or untested combinations unknown instead of inferring compatibility from version numbers. Use [evidence and handoff](references/evidence.md) when producing an audit or coordinated change proposal.

## Decide and stage

Determine whether the proposed change actually crosses an interface. Preserve fixed revisions that serve independent contracts unless their owner demonstrates a reason and a replacement test. For an interface change, ask the provider owner to specify the contract and compatibility window; then give each consumer owner a scoped change request with the exact pin/config/docs affected and its acceptance test. Order provider release and compatibility evidence before consumer pin changes, then stage consumer adoption, environment rollout, and mirror/publication where applicable. An independent package's source tests do not prove a consumer's integration.

Propose rollback for each adopting consumer: preserve the previous artifact, pin, configuration, and state; reconcile work created after switching before restoring them. Check the new pin and its compatibility test in the **same consumer commit**. Declare cross-repository acceptance only after those commits pass their own gates and a real installed-entry end-to-end path succeeds in each targeted environment. If live access is unavailable, report that gate as open; a synthetic test is supporting evidence, not a substitute.

## Action boundary

Read-only investigation and a reviewable plan are the default. Change repositories, installed packages, or runtime configuration only within the user's authorization and each owner's workflow. This skill grants no permission to push, merge, change permissions, or alter another repository. Do not start a standing watcher or require a full scan or paid LLM experiment for every invocation.
