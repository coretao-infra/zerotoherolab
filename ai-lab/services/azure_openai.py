"""azure_openai.py
===================
Adapter around the **Azure OpenAI Image Edit API**.

Responsibilities
----------------
1. Validate that required environment variables are present.
2. Convert the *images/generations* endpoint (Playground copy-paste) to the *images/edits* endpoint required for image-in ➜ image-out.
3. Perform a **multipart/form-data** POST request with the image file and user prompt.
4. Support both possible response formats:
   • **URL** – DALL·E 3 returns a signed URL valid ~24 h.  
   • **base64** – GPT-image-1 returns `b64_json`; the code decodes and stores it under *static/generated/* so Flask can serve it.

Typical usage (already wrapped by ``services.generator``)::

    svc = AzureOpenAIService()
    url = svc.generate_image('static/uploads/photo.png', 'Add a red hat')

The method is stateless so you can keep a single instance for the whole app.
"""

from __future__ import annotations

import os
import uuid
import base64
from typing import Optional

import requests
from flask import url_for

# ---------------------------------------------------------------------------
# Environment configuration – loaded once at import time.
# ---------------------------------------------------------------------------
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")


class AzureOpenAIService:
    """Wrapper class for Azure OpenAI *Image Edit* endpoint."""

    # ---------------------------------------------------------------------
    # Construction / validation
    # ---------------------------------------------------------------------
    def __init__(self) -> None:
        # Fail fast if the developer forgot to set environment variables.
        if not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_API_KEY:
            raise RuntimeError("Azure OpenAI credentials missing – check .env")

        # Replace *generations* with *edits* (Playground copies generations).
        self.edit_endpoint = AZURE_OPENAI_ENDPOINT.replace(
            "/images/generations", "/images/edits"
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def generate_image(
        self,
        image_path: str,
        prompt: str,
        size: str = "1024x1024",
    ) -> Optional[str]:
        """Upload *image_path* & *prompt* to Azure and return output URL.

        Parameters
        ----------
        image_path : str
            Local filesystem path to the uploaded image.
        prompt : str
            Text describing the desired edit.
        size : str, default "1024x1024"
            Output resolution requested (see Azure docs for options).

        Returns
        -------
        str | None
            Publicly accessible URL (Azure or local `/static/generated/*`).
            Returns ``None`` when the API responds with no data.
        """

        # --- Build multipart request ------------------------------------
        with open(image_path, "rb") as img_file:
            files = {
                "image": (
                    os.path.basename(image_path),  # original filename sans path
                    img_file,                       # file-like object
                    "image/png",                   # MIME type (Azure ignores but polite)
                )
            }
            data = {"prompt": prompt, "n": 1, "size": size}
            headers = {"api-key": AZURE_OPENAI_API_KEY}

            # 120-second timeout to accommodate larger edits.
            response = requests.post(
                self.edit_endpoint,
                headers=headers,
                files=files,
                data=data,
                timeout=120,
            )

        # Raise for non-200 to let caller handle/log.
        response.raise_for_status()

        payload = response.json()
        if not payload.get("data"):
            return None  # Unexpected empty result

        item = payload["data"][0]

        # --- Case 1: DALL·E URL ----------------------------------------
        if "url" in item:
            return item["url"]

        # --- Case 2: GPT-image-1 base64 -------------------------------
        if "b64_json" in item:
            # Decode and persist so it can be served as a static asset.
            gen_dir = os.path.join("static", "generated")
            os.makedirs(gen_dir, exist_ok=True)
            img_bytes = base64.b64decode(item["b64_json"])
            filename = f"gen_{uuid.uuid4().hex}.png"
            file_path = os.path.join(gen_dir, filename)
            with open(file_path, "wb") as fh:
                fh.write(img_bytes)
            return url_for("static", filename=f"generated/{filename}")

        # Fallback – unknown schema
        return None
