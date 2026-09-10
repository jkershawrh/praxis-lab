#!/usr/bin/env bash
set -euo pipefail

network="praxis-e2e-${GITHUB_RUN_ID:-local}-$$"
mock="praxis-mock-${GITHUB_RUN_ID:-local}-$$"
gateway="praxis-gateway-${GITHUB_RUN_ID:-local}-$$"
backend_image="praxis-track1-mock:${GITHUB_SHA:-local}"
gateway_image="ghcr.io/praxis-proxy/ai@sha256:ef1f8e216f3428e15bc5953f5938562658edc9232ebfce5f946f05cddd34a0e6"
gateway_secret="gateway-owned-validation-secret"

cleanup() {
  docker rm -f "$gateway" "$mock" >/dev/null 2>&1 || true
  docker network rm "$network" >/dev/null 2>&1 || true
}
trap cleanup EXIT

docker build -t "$backend_image" -f backend/Containerfile backend
docker network create "$network" >/dev/null
docker run -d --name "$mock" --network "$network" \
  -e EXPECTED_API_KEY="$gateway_secret" "$backend_image" >/dev/null
docker run -d --name "$gateway" --network "$network" -p 127.0.0.1::8080 \
  -e MODEL_API_KEY="$gateway_secret" \
  -v "$PWD/config/praxis/track1-ci.yaml:/etc/praxis/praxis-ai.yaml:ro" \
  "$gateway_image" --config /etc/praxis/praxis-ai.yaml >/dev/null

gateway_port="$(docker port "$gateway" 8080/tcp | sed 's/.*://')"
response_file="$(mktemp /tmp/praxis-e2e-response.XXXXXX.json)"
trap 'rm -f "$response_file"; cleanup' EXIT

for attempt in $(seq 1 30); do
  if curl --fail --silent "http://127.0.0.1:${gateway_port}/" >/dev/null; then
    break
  fi
  if [ "$attempt" -eq 30 ]; then
    docker logs "$gateway"
    exit 1
  fi
  sleep 1
done

status="$(curl --silent --output "$response_file" --write-out '%{http_code}' \
  "http://127.0.0.1:${gateway_port}/v1/chat/completions" \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer caller-supplied-wrong-secret' \
  -d '{"model":"lab-model","messages":[{"role":"user","content":"hello"}]}')"

test "$status" = "200"
python3 - "$response_file" <<'PY'
import json
import sys

with open(sys.argv[1]) as stream:
    response = json.load(stream)
assert response["model"] == "lab-model"
assert response["choices"][0]["message"]["role"] == "assistant"
PY

if docker logs "$gateway" 2>&1 | grep -F "$gateway_secret"; then
  echo "Gateway logs exposed the upstream credential" >&2
  exit 1
fi

echo "AMD64 E2E: Praxis replaced caller authorization and routed successfully"
