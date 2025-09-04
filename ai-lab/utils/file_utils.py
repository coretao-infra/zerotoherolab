"""file_utils.py
================
Reusable helpers for **file validation** and **persistence**.

The functions are intentionally framework-agnostic except for importing
`werkzeug.utils.secure_filename` (Flask dependency) and `flask.url_for` to
produce a static URL once the file is saved.
"""

import os
from typing import Tuple

from flask import url_for
from werkzeug.utils import secure_filename

# ---------------------------------------------------------------------------
# Configuration constants
# ---------------------------------------------------------------------------
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}  # lightweight whitelist
UPLOAD_DIR = os.path.join("static", "uploads")  # disk location for originals


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

def allowed_file(filename: str) -> bool:
    """Return ``True`` if *filename* has an allowed extension.

    The check is case-insensitive and does not attempt to validate MIME type;
    that should happen on the server side if required.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_upload(file_storage) -> Tuple[str, str]:
    """Persist an uploaded file and return its *path* and public *URL*.

    Parameters
    ----------
    file_storage : werkzeug.datastructures.FileStorage
        The file object obtained from ``request.files``.

    Returns
    -------
    (path, url) : Tuple[str, str]
        * ``path`` – absolute filesystem path where the file was stored.
        * ``url``  – public URL served by Flask static route (``/static/uploads``).
    """
    # Sanitize the original filename to prevent directory traversal attacks.
    filename = secure_filename(file_storage.filename)

    # Ensure upload directory exists; ``exist_ok=True`` prevents race conditions.
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Construct absolute path and write file to disk.
    path = os.path.join(UPLOAD_DIR, filename)
    file_storage.save(path)

    # Generate URL that templates/frontend can embed.
    return path, url_for("static", filename=f"uploads/{filename}")
