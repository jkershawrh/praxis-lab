#!/usr/bin/env bash
set -euo pipefail

project_name="${PROJECT_NAME:-praxis-ai-gateway}"
lab_key="${LAB_MODEL_API_KEY:-track1-mock-only}"

oc new-project "$project_name" 2>/dev/null || oc project "$project_name"
oc create secret generic model-backend-credentials \
  --from-literal=api-key="$lab_key" \
  --dry-run=client -o yaml | oc apply -f -
oc apply -k deploy/kustomize/base
oc rollout status deployment/mock-backend --timeout=180s
oc rollout status deployment/praxis-ai --timeout=180s
oc rollout status deployment/praxis-ui --timeout=180s
