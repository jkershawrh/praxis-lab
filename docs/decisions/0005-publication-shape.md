# ADR 0005: Publish one quickstart and one progressive lab

## Status

Accepted

## Decision

Maintain one source repository. Publish Track 1 as one standalone quickstart and publish one RHPDS lab containing Tracks 1, 2, and 3 as progressive, independently validated modules.

Track 1 remains usable without Tracks 2 or 3. Later tracks may reuse a validated earlier state, but each track must declare prerequisites and provide its own competency and red/green evidence.

## Rationale

Three quickstarts plus three labs would duplicate manifests, tests, explanations, release pins, and security guidance. A shared repository keeps the backend-neutral contract and upstream evidence consistent while allowing the short adoption experience and the deeper instructor-led experience to have different packaging.

## Consequences

- The repository is the single tested source for both publication formats.
- Quickstart conversion selects Track 1 material only.
- RHPDS conversion builds one catalog item with three navigable tracks.
- MaaS integration stays in the RHPDS deployment overlay and is not part of the conceptual architecture.
- A later track becomes a separate quickstart only after learner demand and maintenance ownership justify extraction.
