# Praxis AI Gateway Lab Design

## Problem statement

Enterprise application teams often integrate directly with individual AI model providers. That distributes credentials, provider URLs, protocol differences, routing logic, and governance policy across many codebases. Platform teams need one governed access layer that lets applications use AI models through a stable interface while operators retain control of upstream configuration.

This project teaches a platform engineer how to establish that access layer with Praxis AI Gateway on Red Hat OpenShift. It demonstrates the behavior with Java, Python, and TypeScript clients and then adds operational and industry-sensitive controls.

## Architectural promise

The invariant taught by every track is:

```text
polyglot clients -> Praxis AI Gateway -> configurable inference backend
```

Clients must not contain an upstream model URL, provider credential, or provider-specific routing policy. Replacing the upstream backend requires gateway or deployment configuration changes only.

## RHPDS MaaS boundary

RHPDS MaaS is a source of model access for a constrained shared lab environment. It is not presented as the target production architecture, a Praxis dependency, or the recommended way to host models.

The RHPDS overlay maps provisioned values into the neutral contract:

| Neutral setting | RHPDS source |
| --- | --- |
| `MODEL_BASE_URL` | `{maas_api_url}` |
| `MODEL_NAME` | `{maas_model}` |
| `MODEL_API_KEY` | an OpenShift Secret populated during provisioning |

An OpenShift AI overlay must satisfy the same contract. Backend substitution is a release-gating portability test.

## Personas

Primary persona: enterprise AI platform engineer.

Secondary personas: application developer, security architect, AI governance lead, and operations engineer.

Primary quickstart industry classification: Media and IT services. Track 3 applies the same platform pattern to Banking and securities, Healthcare provider, Government, Manufacturing, and Telecommunications without asserting regulatory compliance.

## Learning tracks

### Track 1: Establish governed access

Learners will:

1. Observe why direct provider integration creates operational risk.
2. Deploy Praxis AI Gateway on OpenShift.
3. Connect Praxis to a supplied inference endpoint.
4. Store the upstream credential in an OpenShift Secret.
5. Invoke the same logical operation from Java, Python, and TypeScript.
6. Verify health, TLS, routing, and credential isolation.
7. Replace the inference backend without changing client code.

Track 1 is the standalone 30–45 minute quickstart.

### Track 2: Operate a platform capability

Learners begin with stateless OpenAI Responses passthrough, then add supported protocol handling, prompt enrichment, token accounting, PostgreSQL response storage and rehydration, Conversations API behavior, correlated telemetry, OpenShift observability, GitOps reconciliation, and defined failure behavior. Anthropic-to-OpenAI translation is an optional protocol lesson. MCP content is optional and included only when the selected model and pinned Praxis release pass the required tool-loop tests.

### Track 3: Apply governance patterns

Learners configure model allowlists, tenant separation, controlled egress, sensitive-data handling, request evidence, retention boundaries, credential rotation, and fail-open/fail-closed behavior. Scenario profiles explain industry motivations but do not claim that completion establishes compliance. The upstream policy-engine demonstration is treated as preview material because it requires a feature-gated source build and unpublished dependencies.

## Module map

| Module | Track | Competency |
| --- | --- | --- |
| 0. Access and architecture | Foundation | Explain component responsibilities and the MaaS boundary |
| 1. Expose the unmanaged risk | Foundation | Identify distributed credentials and provider coupling |
| 2. Deploy Praxis | 1 | Establish a healthy OpenShift workload |
| 3. Connect a backend | 1 | Configure a model without client coupling |
| 4. Exercise polyglot clients | 1 | Prove equivalent Java, Python, and TypeScript behavior |
| 5. Validate the boundary | 1 | Prove TLS, secret isolation, and backend portability |
| 6. Route by policy | 2 | Apply model-aware routing centrally |
| 7. Account and persist | 2 | Capture usage and response state intentionally |
| 8. Visualize and observe requests | 2 | Correlate the UI topology, routing result, and exact request trace |
| 9. Reconcile with GitOps | 2 | Detect and correct configuration drift |
| 10. Handle failure | 2 | Demonstrate defined timeout and recovery behavior |
| 11. Isolate tenants | 3 | Prevent unauthorized cross-tenant access |
| 12. Apply data controls | 3 | Minimize or reject sensitive content by policy |
| 13. Preserve audit evidence | 3 | Produce attributable request records without secrets |
| 14. Compare industry profiles | 3 | Explain policy trade-offs by scenario |
| 15. Assess the platform | 3 | Demonstrate mastery against the rubric |

## Development loop

Every capability follows the same loop:

1. Define a learner competency.
2. Define an implementation contract.
3. Write a Given/When/Then behavior.
4. Add a failing automated validation (red).
5. Implement the minimum configuration or code.
6. Run validation until it passes (green).
7. Add a runnable example and learner explanation.
8. Refactor without regressing the evidence.

## Red Hat alignment

The reference path prioritizes Red Hat OpenShift, Red Hat OpenShift AI model serving, OpenShift GitOps, OpenShift monitoring and logging capabilities, Red Hat build of Keycloak when identity federation is required, Red Hat Advanced Cluster Security when available, and Universal Base Image-derived application containers where practical.

Components must be described accurately as Red Hat products, upstream projects, partner components, or lab infrastructure. Praxis is an upstream project deployed on OpenShift; this lab must not imply Red Hat product support for Praxis unless separately established.

## Demonstration experience

Track 1 includes a small request/response UI because terminal-only proxy demonstrations obscure the value of the gateway. Track 2 expands it into a topology and evidence view backed by exact-request tracing. The UI is a learning aid, not a replacement for OpenShift observability. Its contract is defined in `docs/ui-observability.md`.

## Release gates

- Track 1 operates independently of Tracks 2 and 3.
- No client contains provider credentials or upstream model URLs.
- Backend replacement changes configuration only.
- All images and dependencies intended for repeatable deployment are pinned.
- Static, contract, unit, integration, security, and publication tests are green where runnable without a cluster.
- A fresh lab validation produces the intended red state.
- Applying the solution produces the corresponding green state.
- Showroom builds without unresolved attributes or missing navigation targets.
- No unsupported performance, security, supportability, or compliance claims are published.
