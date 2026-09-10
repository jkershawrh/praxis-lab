# Track 1 deployment

The base overlay deploys Praxis AI `v0.3.0` and a small UBI-based mock inference backend. The mock makes the first red/green cycle deterministic and avoids consuming shared model capacity.

Create the namespace and its lab-only upstream credential without writing the value to a manifest:

```bash
oc new-project praxis-ai-gateway
oc create secret generic model-backend-credentials \
  --from-literal=api-key="$(openssl rand -hex 24)"
oc apply -k deploy/kustomize/base
```

The OpenShift Route uses edge TLS. Praxis's admin health endpoint remains bound to loopback and is checked with an exec probe; it is not exposed by the Service.

The base Route is suitable for a controlled lab environment because the injected credential authorizes only the mock backend. Before connecting a real model, the deployment must add a trusted downstream authentication boundary. Praxis does not provide that boundary automatically.

The learner UI has its own edge-TLS Route in the mock profile. The RHPDS overlay protects that Route with an OpenShift OAuth proxy sidecar, re-encrypt TLS, a service serving certificate, and a generated cookie secret.

RHPDS MaaS provisioning will replace the mock backend through an overlay. MaaS endpoint and virtual-key mechanics remain provisioning concerns; learner clients continue to use only `PRAXIS_BASE_URL`.

## RHPDS model-access overlay

The RHPDS overlay removes the mock backend and public Route. It renders the provisioned model URL into Praxis configuration and stores the model credential in an OpenShift Secret:

```bash
python3 -m pip install 'PyYAML>=6,<7'
export MODEL_BASE_URL='<provided model endpoint>'
export MODEL_API_KEY='<provided virtual key>'
export PRAXIS_MODEL='<provided model name>'
./deploy/rhpds/deploy.sh
```

Do not place these values in shell history in a shared environment. The final Showroom workflow will receive them as provisioned attributes and avoid displaying the credential.

For Track 1, an authenticated namespace user establishes local access:

```bash
oc port-forward service/praxis-ai 8080:8080
export PRAXIS_BASE_URL=http://127.0.0.1:8080
python3 clients/python/client.py
```

OpenShift authorization governs who can create the port-forward. A public application Route is intentionally absent from the RHPDS overlay until an OAuth/OIDC ingress boundary is added and tested.
