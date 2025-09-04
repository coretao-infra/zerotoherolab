"""
generator.py
================
High-level service that orchestrates the **upload ➜ Azure OpenAI ➜ response** pipeline.

Usage from Flask route::

    from services.generator import generate_from_upload
    
    @app.route('/generate', methods=['POST'])
    def generate_route():
        file = request.files.get('base_image')
        prompt = request.form.get('prompt', '')
        uploaded_url, generated_url = generate_from_upload(file, prompt)
        return jsonify({"uploadedUrl": uploaded_url, "imageUrl": generated_url})

`generate_from_upload` takes the raw Werkzeug `FileStorage` object together with the
user prompt and returns two public URLs:

1. ``uploaded_url`` – location where the original file is served (``/static/uploads/...``)
2. ``generated_url`` – location of the AI-generated image (either Azure URL or local */static/generated/* path)

The function hides all lower-level details: file validation, persistence, and calling
Azure OpenAI. This makes the Flask layer extremely thin and keeps business logic
isolated.
"""

from typing import Tuple, Optional

# Import the Azure OpenAI wrapper (handles REST API & base64 logic)
from services.azure_openai import AzureOpenAIService  # absolute import – package init in __init__.py

# Utility helpers for validation and saving uploads
from utils.file_utils import allowed_file, save_upload

# Create a single service instance (stateless, safe to reuse)
service = AzureOpenAIService()


def generate_from_upload(file_storage, prompt: str) -> Tuple[Optional[str], Optional[str]]:
    """Process an uploaded image and prompt.

    Parameters
    ----------
    file_storage : werkzeug.datastructures.FileStorage | None
        The file object coming from ``request.files['base_image']``.
    prompt : str
        Natural-language instructions describing the desired transformation.

    Returns
    -------
    (uploaded_url, generated_url) : Tuple[str | None, str | None]
        * ``uploaded_url`` – URL for the saved original image (``static/uploads``).
        * ``generated_url`` – URL for the AI-generated output. ``None`` if generation failed.
    """

    # ---- Validate file -----------------------------------------------------
    if not file_storage or not file_storage.filename:
        # Nothing to process – return early to avoid unnecessary work.
        return None, None

    # Ensure the file has an allowed extension (png, jpg, etc.).
    if not allowed_file(file_storage.filename):
        return None, None

    # ---- Persist upload ----------------------------------------------------
    # save_upload() writes the file under *static/uploads/* and returns both the
    # absolute disk path and the public static URL path (served by Flask).
    path, uploaded_url = save_upload(file_storage)

    # ---- Call Azure OpenAI -------------------------------------------------
    # This may raise exceptions (network issues, 400/403 etc.). Caller can catch.
    try:
        generated_url: Optional[str] = service.generate_image(path, prompt)
    except Exception as exc:  # noqa: BLE001 – broad catch fine in service layer
        # In production consider logging stacktrace with logging module.
        print(f"Azure generation failed: {exc}")
        generated_url = None

    # ---- Return -----------------------------------------------------------
    return uploaded_url, generated_url
