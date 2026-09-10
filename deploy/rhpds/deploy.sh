#!/usr/bin/env bash
set -euo pipefail

: "${MODEL_BASE_URL:?MODEL_BASE_URL is required}"
: "${MODEL_API_KEY:?MODEL_API_KEY is required}"

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
oc create configmap praxis-ai-config \
  --from-file=praxis-ai.yaml="$rendered_config" \
  --dry-run=client -o yaml | oc apply -f -
oc apply -k deploy/kustomize/overlays/rhpds
oc rollout status deployment/praxis-ai --timeout=180s

printf '%s\n' "Praxis is available to authorized namespace users with:"
printf '%s\n' "  oc port-forward service/praxis-ai 8080:8080"

