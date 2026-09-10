"""Small OpenAI-compatible backend used to test Praxis without consuming a model."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import time
import uuid


def build_response(path, payload):
    model = payload.get("model", "mock-model")
    if path == "/v1/chat/completions":
        return 200, {
            "id": f"chatcmpl-{uuid.uuid4().hex}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "Praxis routed this response through the mock backend.",
                    },
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
        }
    return 404, {"error": {"message": "not found", "type": "invalid_request_error"}}


class Handler(BaseHTTPRequestHandler):
    server_version = "praxis-track1-mock"

    def do_GET(self):
        if self.path == "/healthz":
            self.respond(200, {"status": "ok"})
        else:
            self.respond(404, {"error": {"message": "not found", "type": "invalid_request_error"}})

    def do_POST(self):
        expected = os.environ.get("EXPECTED_API_KEY", "")
        supplied = self.headers.get("Authorization", "")
        if expected and supplied != f"Bearer {expected}":
            self.respond(401, {"error": {"message": "unauthorized", "type": "authentication_error"}})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            self.respond(400, {"error": {"message": "invalid JSON", "type": "invalid_request_error"}})
            return

        self.respond(*build_response(self.path, payload))

    def respond(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, message, *args):
        # Do not log headers or bodies; tests use only method/path/status evidence.
        print(f'{self.command} {self.path} - {message % args}', flush=True)


def main():
    port = int(os.environ.get("PORT", "8000"))
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()


if __name__ == "__main__":
    main()

