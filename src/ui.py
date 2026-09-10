"""Track 1 learner UI for the backend-neutral Praxis client contract."""

import json
import os
import secrets
import time

import httpx


TOPOLOGY = """
<div class="praxis-flow" aria-label="Request path">
  <span>Application client</span><strong>→</strong>
  <span>Praxis AI Gateway</span><strong>→</strong>
  <span>Configured model backend</span>
</div>
<p><small>The backend endpoint and its credential remain gateway-side configuration.</small></p>
"""


def new_traceparent():
    return f"00-{secrets.token_hex(16)}-{secrets.token_hex(8)}-01"


def invoke(prompt, model, base_url=None, timeout=30.0):
    endpoint = (base_url or os.environ.get("PRAXIS_BASE_URL", "http://127.0.0.1:8080")).rstrip("/")
    traceparent = new_traceparent()
    started = time.monotonic()
    try:
        response = httpx.post(
            f"{endpoint}/v1/chat/completions",
            headers={"Content-Type": "application/json", "traceparent": traceparent},
            json={
                "model": model or os.environ.get("PRAXIS_MODEL", "lab-model"),
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=timeout,
        )
        elapsed_ms = round((time.monotonic() - started) * 1000, 1)
        try:
            body = response.json()
        except ValueError:
            body = {"error": {"message": "The gateway returned a non-JSON response."}}
        summary = {
            "status": response.status_code,
            "elapsed_ms": elapsed_ms,
            "trace_id": traceparent.split("-")[1],
            "model": body.get("model", model),
        }
        return summary, body
    except httpx.HTTPError as error:
        elapsed_ms = round((time.monotonic() - started) * 1000, 1)
        return {
            "status": "unavailable",
            "elapsed_ms": elapsed_ms,
            "trace_id": traceparent.split("-")[1],
            "model": model,
        }, {"error": {"message": str(error), "type": "gateway_connection_error"}}


def build_ui():
    import gradio as gr

    with gr.Blocks(title="Praxis AI Gateway Lab") as app:
        gr.Markdown("# Praxis AI Gateway: governed model access")
        gr.HTML(TOPOLOGY)
        with gr.Tab("Request"):
            prompt = gr.Textbox(
                label="Prompt",
                value="Explain the role of an AI gateway in one sentence.",
                lines=3,
            )
            model = gr.Textbox(label="Logical model", value=os.environ.get("PRAXIS_MODEL", "lab-model"))
            submit = gr.Button("Send through Praxis", variant="primary")
            evidence = gr.JSON(label="Request evidence")
            response = gr.JSON(label="Sanitized response")
            submit.click(invoke, inputs=[prompt, model], outputs=[evidence, response])
        with gr.Tab("What to observe"):
            gr.Markdown(
                "The application sends no upstream credential. Praxis selects the configured "
                "backend and replaces any caller-supplied authorization before forwarding. "
                "Track 2 will connect each request's exact trace ID to topology evidence."
            )
        gr.Markdown("AI-generated output can be inaccurate. Verify important results.")
    return app


if __name__ == "__main__":
    build_ui().launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("UI_PORT", "7860")),
    )
