"""
main.py
=========
Flask entry-point for the **AI Image Generator**.

This file purposefully stays <50 LOC by delegating heavy logic
(upload validation, OpenAI calls, etc.) to `services/`.

Key routes
----------
/            → GET  – serve HTML UI (`templates/index.html`)
/generate    → POST – receive *multipart* (file + prompt) and return JSON
               with URLs used by front-end JS.

Environment is loaded early via **python-dotenv** so that downstream service
modules can read `AZURE_OPENAI_*` immediately when imported.
"""

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# 1. Configuration – load .env before importing anything else that depends on it
# ---------------------------------------------------------------------------
load_dotenv()  # pulls variables into os.environ

# Import after env is ready (service needs API key)
from services.generator import generate_from_upload  # noqa: E402 – import after dotenv

# ---------------------------------------------------------------------------
# 2. Flask application setup
# ---------------------------------------------------------------------------
app = Flask(__name__)


# ---------------------------------------------------------------------------
# 3. Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    """Render the HTML SPA (single-page app)."""
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_route():
    """Receive AJAX request, orchestrate generation, reply JSON.

    The body is `multipart/form-data` containing:
      • **base_image** – FileStorage
      • **prompt**     – str
    """
    file = request.files.get("base_image")
    prompt = request.form.get("prompt", "")

    # Delegate to high-level service – returns (uploaded_url, generated_url)
    uploaded_url, generated_url = generate_from_upload(file, prompt)

    return jsonify({"uploadedUrl": uploaded_url, "imageUrl": generated_url})


# ---------------------------------------------------------------------------
# 4. Dev server bootstrap
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Debug enabled for hot-reload during development. Disable in prod.
    app.run(debug=True)
