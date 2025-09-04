/**
 * app.js
 * ======
 * Front-end controller for the AI Image Generator UI.
 *
 * Responsibilities
 * --------------
 * 1. Local **preview** of the uploaded image (via FileReader).
 * 2. Submit the form via **AJAX** (fetch → /generate).
 * 3. Manage UI states: disable button, show spinner class, show skeleton loader.
 * 4. Render both uploaded & generated images side-by-side once ready.
 *
 * No external dependencies – pure vanilla JS.
 */

// ---------------------------------------------------------------------------
// DOM references (cached once – avoids repeated lookups)
// ---------------------------------------------------------------------------
/* eslint-disable no-undef */
const form = document.getElementById('gen-form'); // <form>
const btn = document.getElementById('gen-btn'); // <button>
const results = document.getElementById('results'); // flex container for two columns
const uploadedImg = document.getElementById('uploaded-img'); // <img> showing original
const generatedImg = document.getElementById('generated-img'); // <img> showing AI result
const skeleton = document.getElementById('skeleton'); // shimmering placeholder
const fileInput = document.getElementById('base_image'); // <input type=file>
/* eslint-enable no-undef */

// ---------------------------------------------------------------------------
// 1. Local preview handler ---------------------------------------------------
// ---------------------------------------------------------------------------
fileInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (!file) return; // User cleared selection

  // FileReader → Base64 URL → <img src> => instant preview without upload
  const reader = new FileReader();
  reader.onload = (ev) => {
    uploadedImg.src = ev.target.result; // display preview
    results.style.display = 'flex'; // make row visible

    // Reset generated placeholder state (fresh session)
    skeleton.style.display = 'none';
    generatedImg.style.display = 'none';
  };
  reader.readAsDataURL(file);
});

// ---------------------------------------------------------------------------
// 2. Form submit (AJAX) ------------------------------------------------------
// ---------------------------------------------------------------------------
form.addEventListener('submit', async (e) => {
  e.preventDefault(); // disable default page reload

  // ---------------- UI: loading state -----------------------------------
  btn.disabled = true;
  btn.classList.add('loading'); // CSS adds spinner via ::after

  // Match skeleton size to preview to avoid layout shift
  skeleton.style.width = `${uploadedImg.clientWidth}px`;
  skeleton.style.height = `${uploadedImg.clientHeight}px`;
  skeleton.style.display = 'block';
  generatedImg.style.display = 'none';

  // ---------------- Network: send multipart ----------------------------
  try {
    const response = await fetch('/generate', {
      method: 'POST',
      body: new FormData(form), // FormData picks up file + prompt
    });
    const data = await response.json();

    // ---------------- UI: success path --------------------------------
    if (data.imageUrl) {
      generatedImg.src = data.imageUrl;
      generatedImg.style.display = 'block';
      skeleton.style.display = 'none';
    }
  } catch (err) {
    // eslint-disable-next-line no-console
    console.error('Generation failed:', err);
    alert('Image generation failed. Please try again.');
  } finally {
    // ---------------- UI: restore button ------------------------------
    btn.disabled = false;
    btn.classList.remove('loading');
  }
});
