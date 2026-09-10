# ADR 0001: Use a backend-neutral inference contract

Status: accepted

## Context

RHPDS supplies shared model access through MaaS, while enterprise deployments may use Red Hat OpenShift AI model serving or another approved endpoint. Teaching MaaS-specific configuration would couple the learning outcome to demo infrastructure.

## Decision

Praxis consumes `MODEL_BASE_URL`, `MODEL_NAME`, and a credential referenced from an OpenShift Secret. Clients consume only the Praxis route. RHPDS MaaS and OpenShift AI are deployment overlays implementing the same contract.

## Consequences

Backend portability becomes testable. RHPDS provisioning details remain outside client code and core learner outcomes. Any provider-specific feature must be isolated behind an explicit, optional profile.

