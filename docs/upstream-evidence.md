# Upstream Evidence Review

Reviewed on 2026-09-10.

## Sources and pins

| Source | Reviewed revision | Use in this project |
| --- | --- | --- |
| `praxis-proxy/ai` | v0.3.0, `b44360afb4100c5543b1180ac8df16e482978fc8` | Released configuration and runtime authority |
| `praxis-proxy/demos` | `fe0c1e7dc26ae54462f5e844b6beb9e00dcf9e10` | Runnable examples and learning-sequence evidence |
| `praxis-proxy/experimental` | `ff252a5febd5f09a8fe9c3a55d624520de37163d` | Preview-only ideas; never a core dependency |
| Praxis organization projects | Five open project boards as viewed on 2026-09-10 | Directional roadmap context only |
| AI Gateway presentations document | Not reviewed | Direct export returned HTTP 401; access is required before using it as evidence |

## What the demos support

The upstream demos provide concrete flows for:

- Stateless OpenAI Responses passthrough, including streaming.
- Non-streaming response storage and multi-turn rehydration.
- Streaming multi-turn response handling.
- Local OpenAI Conversations CRUD using SQLite, with PostgreSQL described as supported.
- Anthropic Messages passthrough and translation to OpenAI Chat Completions.
- Server-side MCP tool loops.
- File resolution and search flows.
- A feature-gated policy-engine build integrating identity, policy decisions, redaction, audit, session taint, token exchange, and human approval.
- Several Praxis Grid and MaaS integration environments.

These demos are upstream evidence that a capability has been exercised. Each selected lab capability still needs a pinned configuration, an OpenShift test, and local red/green evidence in this repository.

## Core lab decisions

1. Track 1 remains intentionally simple: health, routing, upstream credential replacement, TLS, and polyglot client isolation.
2. Track 2 should prefer the stateless Responses flow first, then add persistence and Conversations as separate competencies.
3. Anthropic-to-OpenAI translation is a strong optional Track 2 demonstration of why applications benefit from a protocol-aware gateway.
4. The MCP agentic loop belongs in an optional advanced module because it requires model tool-calling behavior and additional runtime services.
5. The policy-engine demo is compelling for industry scenarios but requires a custom source build and unpublished feature dependencies. It must be labeled preview and cannot anchor the baseline Track 3 release.
6. Grid, cloud bursting, distributed rate limiting, and Switchyard routing remain outside the core lab until promoted and qualified independently.

## MaaS interpretation

The upstream MaaS IPP demo is an integration-development environment. It reproduces a MaaS data path and explicitly delegates filter ownership to the MaaS controller. This does not change this lab's architectural boundary: RHPDS MaaS supplies model access, while learner applications call Praxis through a backend-neutral contract.

## Roadmap interpretation

The organization exposes five open project areas: AI Grid, distributed inference, model serving, agentic capabilities, and load balancing. Project-board presence signals planned or active work, not released behavior. Roadmap items can inform “what next” material but cannot appear as guaranteed learning outcomes.

## Claim control

Upstream demo performance observations are not copied into this project's claims. Any latency, throughput, token, capacity, or overhead claim must be measured again on the target Intel RHPDS environment and entered in `tests/claim_registry.yaml`.

