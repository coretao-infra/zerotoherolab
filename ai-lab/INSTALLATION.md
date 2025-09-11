# Installation Guide – AI Image Generator Lab

Follow these steps to set up and run the project locally. Estimated time: **5 minutes**.

---

## 1. Prerequisites
- **Python 3.8+**  
  Verify: `python --version`
- **Git** for cloning the repository
- An **Azure OpenAI** resource with an *Image Edit* capable deployment (DALL·E 3 or GPT-image-1). Obtain:
  1. **Endpoint URL** (ending with `/images/generations?...`)
  2. **API key**

---

## 2. Clone the repository
```bash
$ git clone https://github.com/<your-org>/ai-image-generator-lab.git
$ cd ai-image-generator-lab/final-version
```

---

## 3. Create & activate a virtual environment (recommended)
```bash
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

---

## 4. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 5. Configure environment variables
1. Duplicate the sample env file:
   ```bash
   copy .env.example .env   # Windows
   # or
   cp .env.example .env     # macOS / Linux
   ```
2. Open `.env` in a text editor and fill in:
   ```env
   AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com/openai/deployments/<deployment>/images/generations?api-version=2025-04-01-preview
   AZURE_OPENAI_API_KEY=<your-key>
   ```

---

## 6. Run the development server
```bash
python main.py
```
Console output:
```
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
```

---

## 7. Test the app
1. Open `http://localhost:5000` in your browser.
2. Click **Upload a base image** and pick a PNG/JPG/GIF/WebP (<20 MB).
3. Enter a prompt, e.g. *"Add a futuristic cyberpunk skyline in the background"*.
4. Click **Generate**.
5. Observe spinner ➜ skeleton ➜ generated image.

---

## 8. Troubleshooting
| Problem                                          | Fix                                                                                       |
| ------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| `RuntimeError: Azure OpenAI credentials missing` | Verify `.env` values and restart.                                                         |
| 400 `unknown_parameter` from Azure               | API version changed – update endpoint or upgrade code.                                    |
| Images not displaying                            | Ensure `static/uploads/` & `static/generated/` exist and are not blocked by `.gitignore`. |

---

## 9. Deactivate virtual environment (when done)
```bash
deactivate
```

---

Enjoy creating AI-powered images locally! For advanced deployment (Docker, Azure App Service, etc.) see the `README.md` in root.
`