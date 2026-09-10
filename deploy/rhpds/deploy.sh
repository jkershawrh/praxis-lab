#!/usr/bin/env bash
set -euo pipefail

: "${MODEL_BASE_URL:?MODEL_BASE_URL is required}"
: "${MODEL_API_KEY:?MODEL_API_KEY is required}"
: "${PRAXIS_MODEL:?PRAXIS_MODEL is required}"

project_name="${PROJECT_NAME:-praxis-ai-gateway}"
rendered_config="$(mktemp /tmp/praxis-ai-config.XXXXXX.yaml)"
trap 'rm -f "$rendered_config"' EXIT

python3 deploy/rhpds/render_config.py \
  --model-base-url "$MODEL_BASE_URL" \
  --output "$rendered_config"

oc new-project "$project_name" 2>/dev/null || oc project "$project_name"
oc create secret generic model-backend-credentials \
  --from-literal=api-key="$MODEL_API_KEY" \
  --dry-run=client -o yaml | oc apply -f -
oc create secret generic praxis-ui-proxy-cookie \
  --from-literal=session_secret="$(openssl rand -base64 32)" \
  --dry-run=client -o yaml | oc apply -f -
oc create configmap praxis-ai-config \
  --from-file=praxis-ai.yaml="$rendered_config" \
  --dry-run=client -o yaml | oc apply -f -
oc apply -k deploy/kustomize/overlays/rhpds
oc set env deployment/praxis-ui PRAXIS_MODEL="$PRAXIS_MODEL"
oc rollout status deployment/praxis-ai --timeout=180s
oc rollout status deployment/praxis-ui --timeout=180s

printf '%s\n' "Authenticated learner UI: https://$(oc get route praxis-ui -o jsonpath='{.spec.host}')"
printf '%s\n' "Direct Praxis access remains limited to authorized namespace port-forward users."
