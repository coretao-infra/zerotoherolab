/**
 * preview.js
 * ==========
 * Lightweight module dedicated to **instant image preview**.
 *
 * The file input in `index.html` has an `onchange` listener wired up by
 * `static/app.js`. When the user selects a file we:
 *   1. Read the image with `FileReader` as a base64 data-URL (runs locally).
 *   2. Inject the data-URL into `<img id="preview-img">` so users get
 *      immediate visual feedback *before* hitting **Generate**.
 *
 * This improves UX by ensuring the correct file has been selected and avoids
 * an unnecessary round-trip to the server.
 */

/**
 * Render the selected image into the preview container.
 *
 * @param {Event} event – `change` event emitted by the `<input type="file">`.
 */
function previewImage(event) {
  const input = event.target; // <input type=file>
  const previewContainer = document.getElementById('preview-container');
  const previewImg = document.getElementById('preview-img');

  // Guard: handle *clear* action where no file is selected.
  if (!input.files || !input.files[0]) {
    previewImg.src = '';
    previewContainer.style.display = 'none';
    return;
  }

  // Only need a single file – grab first.
  const file = input.files[0];

  // FileReader asynchronously converts file → base64 data URL.
  const reader = new FileReader();
  reader.onload = (e) => {
    previewImg.src = e.target.result; // Set <img src="data:image/png;base64,...">
    previewContainer.style.display = 'block'; // Unhide container
  };
  reader.readAsDataURL(file);
}

// Export for unit testing or if using module bundlers (harmless in browser).
// eslint-disable-next-line no-undef
if (typeof module !== 'undefined') {
  module.exports = { previewImage };
}
