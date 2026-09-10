# ADR 0006: Protect the real-backend learner UI with OpenShift OAuth

## Status

Accepted

## Decision

Package the Gradio learner UI as a non-root UBI container. The deterministic mock profile may expose it through an edge-TLS Route because its upstream credential has no external value. The RHPDS real-backend profile must place an OpenShift OAuth proxy sidecar in front of the UI, use a re-encrypt Route and service serving certificate, and remove the direct Praxis Route.

The OAuth proxy does not forward the user's bearer token to Gradio. The UI continues to call only the internal Praxis Service, and Praxis owns the upstream model credential.

## Consequences

- Anonymous users cannot spend the provisioned model budget through the RHPDS UI.
- OpenShift identity and namespace access remain deployment concerns rather than Praxis features.
- A generated cookie secret is required during deployment and is never stored in Git.
- The OAuth proxy is an OpenShift upstream component pinned to its reviewed AMD64 image digest.
