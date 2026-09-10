# Learner UI and Observability Contract

## Purpose

Proxy behavior is difficult to demonstrate from terminal output alone. The learner UI must make the request path, routing decision, and supporting evidence visible without pretending to be a production operations console.

## Progressive experience

### Track 1: Request and response

The UI provides one form that invokes the same client contract used by Java, Python, and TypeScript. It shows:

- The Praxis endpoint, never the upstream endpoint or credential.
- Selected logical model.
- HTTP outcome and elapsed time.
- Sanitized response.
- A simple static path: client → Praxis → configured model backend.

Track 1 does not require a tracing backend.

### Track 2: Topology and exact-request evidence

The UI adds:

- A topology view with visually distinct client, Praxis, and backend responsibilities.
- The route/model selected by Praxis when exposed through approved response metadata.
- A unique W3C `traceparent` for each request.
- Exact trace-ID lookup rather than association with the newest trace.
- A link to the browser-reachable trace view and a separate server-side query endpoint.
- A clear pending/unavailable state when a trace has not arrived.
- Failure-path visualization that distinguishes gateway rejection, connection failure, backend rejection, and backend success.

The UI must never display authorization headers, API keys, raw secrets, cookies, or unredacted sensitive prompt content.

### Track 3: Policy decisions

Where released capabilities support it, the UI may add sanitized policy evidence:

- Allow or deny.
- Policy/rule identifier.
- Tenant and logical model identifiers.
- Whether content was rejected or transformed.
- Whether an approval is required.

Preview policy-engine demonstrations must be labeled preview and remain optional.

## Trust boundaries

The browser must not query a cluster-local trace service directly. A server-side component queries the internal trace endpoint, while generated links use a separately configured browser-reachable URL. UI authentication and trace-service authorization are deployment responsibilities.

## Acceptance criteria

1. Each UI request has a unique trace ID.
2. A displayed trace is retrieved by that exact ID.
3. The displayed topology agrees with response metadata and trace evidence.
4. Missing trace data is shown as missing, never inferred from another request.
5. The UI works without tracing in Track 1.
6. Secrets and raw authorization data never enter UI state or logs.
7. Equivalent API requests remain possible without the UI.

