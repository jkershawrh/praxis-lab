#!/usr/bin/env bash
set -euo pipefail

network="praxis-e2e-${GITHUB_RUN_ID:-local}-$$"
mock="praxis-mock-${GITHUB_RUN_ID:-local}-$$"
gateway="praxis-gateway-${GITHUB_RUN_ID:-local}-$$"
backend_image="praxis-track1-mock:${GITHUB_SHA:-local}"
gateway_image="ghcr.io/praxis-proxy/ai@sha256:ef1f8e216f3428e15bc5953f5938562658edc9232ebfce5f946f05cddd34a0e6"
gateway_secret="gateway-owned-validation-secret"
gateway_port="$((20000 + ($$ % 20000)))"
response_file="$(mktemp /tmp/praxis-e2e-response.XXXXXX.json)"
runtime_config="$(mktemp /tmp/praxis-e2e-config.XXXXXX.yaml)"

cleanup() {
  docker rm -f "$gateway" "$mock" >/dev/null 2>&1 || true
  docker network rm "$network" >/dev/null 2>&1 || true
  rm -f "$response_file" "$runtime_config"
}
trap cleanup EXIT

docker build -t "$backend_image" -f backend/Containerfile backend
docker network create "$network" >/dev/null
docker run -d --name "$mock" --network "$network" \
  -e EXPECTED_API_KEY="$gateway_secret" "$backend_image" >/dev/null
mock_ip="$(docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$mock")"
sed "s/mock-backend/${mock_ip}/" config/praxis/track1-ci.yaml >"$runtime_config"
docker run -d --name "$gateway" --network "$network" -p "127.0.0.1:${gateway_port}:8080" \
  -e MODEL_API_KEY="$gateway_secret" \
  -v "$runtime_config:/etc/praxis/praxis-ai.yaml:ro" \
  "$gateway_image" --config /etc/praxis/praxis-ai.yaml >/dev/null

for attempt in $(seq 1 30); do
  # Any HTTP response proves the listener is ready; Praxis does not promise a 2xx root route.
  if curl --silent --output /dev/null "http://127.0.0.1:${gateway_port}/"; then
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

if [ "$status" != "200" ]; then
  echo "Expected gateway status 200, received $status" >&2
  cat "$response_file" >&2
  docker logs "$gateway" >&2
  docker logs "$mock" >&2
  exit 1
fi
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
