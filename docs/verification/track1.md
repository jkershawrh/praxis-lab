# Track 1 Verification Record

## Pinned inputs

- Praxis AI release: `v0.3.0`
- Source commit: `b44360afb4100c5543b1180ac8df16e482978fc8`
- AMD64 image manifest: `sha256:ef1f8e216f3428e15bc5953f5938562658edc9232ebfce5f946f05cddd34a0e6`
- Upstream image base: Alpine 3.24
- Mock-backend base: Red Hat Universal Base Image 9 Python 3.12, tag `9.6`

## Verified locally

- Six contract tests pass.
- Eight infrastructure tests pass.
- Twelve unit tests pass across the mock backend, RHPDS renderer, and learner UI.
- One Track 1 configuration integration test passes.
- Five publication-readiness tests pass.
- The base Kustomize overlay renders the gateway, UBI learner UI, mock backend, routes, and required network controls without an error.
- The RHPDS overlay renders four resources, removes the mock backend and public Route, and retains the Secret reference.
- The RHPDS configuration renderer accepts supported HTTP(S) endpoint forms and rejects credentials, query strings, fragments, and unsupported paths in model URLs.
- The Java client compiles with the local JDK.

## Verified on AMD64 CI

- GitHub Actions run `34479253005` completed successfully on `ubuntu-24.04` AMD64.
- The pinned Praxis image executed its native `--validate` command successfully against `config/praxis/track1-mock.yaml`.
- GitHub Actions run `34482755952` completed successfully on `ubuntu-24.04` AMD64.
- The runtime test sent a live request through Praxis to the UBI mock backend and received an OpenAI-compatible response.
- The mock backend accepted only the gateway-owned credential even though the caller supplied a different authorization value.
- The runtime test found no gateway-owned credential in Praxis logs.
- The static job passed all 32 tests and rendered both Kustomize overlays.

## Verified on OpenShift

The current test environment is Oberon, `https://api.oberon.fm2aihpcsed.com:6443`, project `praxis-ai-gateway`. Recorded 2026-10-12 with `./runtime-automation/track1/solve.sh` and the pinned `v0.3.0` image.

- Before the project existed, `validate.py` returned `"state": "red"`.
- After `solve.sh`, it returned `"state": "green"`.
- The single worker, `oberon`, is AMD64. `mock-backend`, `praxis-ai`, and `praxis-ui` are Ready under `restricted-v2`.
- A caller-supplied authorization header returned the mock assistant message. The gateway key was absent from Praxis logs.
- Java, Python, and TypeScript clients each returned that same message through a port-forward.
- The learner UI route returned HTTP 200 over HTTPS. Submitting the form through the UI API returned status 200, model `lab-model`, a trace id, and the mock assistant message in 27.9 ms.
- Both routes terminate TLS at the edge and redirect insecure traffic.

An earlier same-day run on `ocpv-infra01` in `intel-rh-demo` found two defects that are now fixed in the manifests: the lab config omitted the admin listener on `127.0.0.1:9901`, and DNS egress allowed port 53 but not the OpenShift DNS pod port 5353. Those lab objects were deleted. The pre-existing demo deployments on that cluster were not deleted. `ocpv-infra01` is not the test target.

## Still open

- Showroom service account port-forward permissions. Oberon has no Showroom, learner, or RHDP service account. The namespaces `rhdp-serviceaccounts` and `showroom-soundcheck-dev` are on `ocpv-infra01`, and this test no longer uses that cluster.
- An ARM Praxis image. Tags `0.3.0` through `0.6.0` publish `linux/amd64` only. Oberon cannot run an ARM image.

## Security boundary

The base Route fronts a mock backend whose credential has no external value. Do not replace the mock with a real model endpoint until a trusted downstream authentication and authorization boundary is added. Praxis upstream documentation assigns client authentication to the deployment.
