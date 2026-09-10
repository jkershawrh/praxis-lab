# ADR 0004: Pin Praxis AI v0.3.0 for Track 1

Status: accepted

## Context

Praxis AI is pre-1.0 and its main branch changes frequently. Reproducible exercises require one reviewed release. The upstream release artifact is an OCI image built on Alpine and currently publishes an AMD64 image.

## Decision

Track 1 pins Praxis AI `v0.3.0`, source commit `b44360afb4100c5543b1180ac8df16e482978fc8`, and AMD64 image manifest digest `sha256:ef1f8e216f3428e15bc5953f5938562658edc9232ebfce5f946f05cddd34a0e6`.

The upstream image is used initially because it is the project's supported release artifact, runs as a non-root user, and includes its health endpoint. It is described as an upstream Alpine image, not a UBI image or Red Hat-supported component.

## Consequences

The target RHPDS worker architecture must be AMD64. A UBI-based rebuild is a future, separately validated overlay and must retain upstream licensing and demonstrate behavioral equivalence. Praxis upgrades require rerunning configuration, protocol, security, and lab evidence before changing this pin.

