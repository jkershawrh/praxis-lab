# Track 1 Verification Record

## Pinned inputs

- Praxis AI release: `v0.3.0`
- Source commit: `b44360afb4100c5543b1180ac8df16e482978fc8`
- AMD64 image manifest: `sha256:ef1f8e216f3428e15bc5953f5938562658edc9232ebfce5f946f05cddd34a0e6`
- Upstream image base: Alpine 3.24
- Mock-backend base: Red Hat Universal Base Image 9 Python 3.12, tag `9.6`

## Verified locally

- Six contract tests pass.
- Four infrastructure tests pass.
- Three mock-backend unit tests pass.
- One Track 1 configuration integration test passes.
- Two publication-foundation tests pass.
- The base Kustomize overlay renders ten OpenShift/Kubernetes resources without an error.
- The RHPDS overlay renders four resources, removes the mock backend and public Route, and retains the Secret reference.
- The RHPDS configuration renderer accepts supported HTTP(S) endpoint forms and rejects credentials, query strings, fragments, and unsupported paths in model URLs.
- The Java client compiles with the local JDK.

## Verified on AMD64 CI

- GitHub Actions run `34479253005` completed successfully on `ubuntu-24.04` AMD64.
- The pinned Praxis image executed its native `--validate` command successfully against `config/praxis/track1-mock.yaml`.
- The static job installed the project tooling, passed all test stages, and rendered both Kustomize overlays.

## Pending OpenShift evidence

- Restricted-v2 Security Context Constraints admission.
- Readiness and liveness behavior.
- Route TLS behavior.
- Praxis-to-backend credential replacement.
- End-to-end Java, Python, and TypeScript parity.
- Fresh validate (red), solve, and final validate (green).
- Confirmation that the Showroom service account has only the minimum port-forward permissions required by Track 1.

The local host is ARM64 while the published Praxis `v0.3.0` image is AMD64-only. An attempted emulated image pull could not complete because the local Podman machine ran out of storage. This is an environment limitation, not positive runtime evidence; configuration remains `verified-local` only at the static-contract level until executed on an AMD64 environment.

## Security boundary

The base Route fronts a mock backend whose credential has no external value. Do not replace the mock with a real model endpoint until a trusted downstream authentication and authorization boundary is added. Praxis upstream documentation assigns client authentication to the deployment.
