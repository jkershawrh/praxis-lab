# ADR 0003: Use one progressive implementation with selectable tracks

Status: accepted

## Context

Track 1 must work as a quickstart, while advanced learners need operational and industry-sensitive material. Duplicating deployments for each track would create drift and obscure progression.

## Decision

Use one base deployment and progressive overlays for Tracks 1–3. Track 1 has no dependency on later tracks. Track 2 depends on Track 1, and Track 3 depends on the relevant Track 1 and Track 2 competencies. Showroom navigation may expose the advanced tracks selectively.

## Consequences

Every overlay requires an idempotent upgrade and validation path. Cleanup must handle both individual tracks and the complete stack.

