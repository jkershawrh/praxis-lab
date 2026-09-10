# Capability and Alignment Matrix

This matrix is a design control. Each capability must be verified against the pinned Praxis release and the target Red Hat platform version before implementation or publication.

| Capability | Praxis responsibility | Red Hat platform responsibility | Maturity source | Track | Required evidence |
| --- | --- | --- | --- | --- | --- |
| Request classification and routing | Inspect and route supported AI requests | Provide scheduling, networking, and configuration | Released v0.3.0 | 1–2 | Contract and integration tests |
| Credential injection | Replace caller credentials with an upstream credential | Store and inject secrets securely | Released v0.3.0 | 1 | Secret scan and pod inspection |
| Health and readiness | Expose gateway health behavior | Enforce probes and rollout health | Released v0.3.0 | 1 | Readiness and failure tests |
| External TLS | Support configured listener/upstream TLS | Route, certificate, and service networking | Released core capability | 1 | TLS verification |
| Stateless Responses passthrough | Classify and route `store: false` requests | Provide a reachable compatible model | Released and upstream demo | 2 | Non-streaming and SSE fixtures |
| Anthropic protocol handling | Validate, route, or translate supported Messages requests | Provide reachable inference service | Released and upstream demo | 2 | Protocol and transformation tests |
| Prompt enrichment | Apply configured gateway filter | Supply declarative configuration | Released v0.3.0 | 2 | Before/after request fixture |
| Token accounting | Extract supported usage data | Collect and visualize telemetry | Released v0.3.0 | 2 | Metrics or structured-log assertion |
| Response storage and rehydration | Manage supported response state | Run and protect PostgreSQL | Released and upstream demos | 2 | Multi-turn persistence and restart test |
| Conversations API | Handle supported CRUD operations locally | Run and protect persistent storage | Released and upstream demo | 2 | CRUD and audit-retention tests |
| Observability | Emit gateway signals | Collect metrics and logs with OpenShift facilities | Released architecture; experimental benchmark exists | 2 | Correlated request evidence |
| Configuration reconciliation | Consume deterministic configuration | Reconcile desired state through OpenShift GitOps | Platform pattern | 2 | Drift test |
| Agentic MCP loop | Resolve and dispatch tools through a server-side loop | Provide runtime identity and network controls | Released and upstream demo | 3 optional | Version-gated loop tests |
| Tenant/model policy | Enforce configured gateway rules | Isolate namespaces, identities, and networks | Feature-gated source-build demo | 3 preview | Positive and negative authorization tests |
| Sensitive-data policy | Redact or reject fields through the policy path | Provide identity, policy, and audit dependencies | Feature-gated source-build demo | 3 preview | Redaction/rejection fixtures |
| Grid/cloud-burst routing | Coordinate distributed providers | Provide multi-cluster networking and telemetry | Roadmap and experimental demos | Excluded from core lab | Separate experimental qualification |
| Switchyard mixture-of-models | Route using an experimental external filter | Provide backend services | Experimental repository | Excluded from core lab | Separate experimental qualification |

## Verification states

- `proposed`: identified from documentation but not tested.
- `verified-local`: reproduced with the pinned Praxis binary or image.
- `verified-openshift`: reproduced on the target OpenShift version.
- `lab-ready`: automated red/green evidence and learner content both pass review.

All capabilities begin in `proposed`. No capability should appear as a guaranteed learner outcome until it reaches `verified-openshift`.

“Upstream demo” means runnable material exists in `praxis-proxy/demos`; it does not by itself establish production support. “Feature-gated source-build demo” means the demo states that no published Praxis build includes all required features. “Experimental” and “roadmap” capabilities cannot become required lab steps.
