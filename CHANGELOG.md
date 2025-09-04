# Changelog

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](https://semver.org/).

---

## [1.1.0] - 2025-09-04
### Added
- Full modularization: introduced `services/` and `utils/` packages.
- New service wrappers (`azure_openai.py`, `generator.py`) with rich docstrings.
- Front-end separated into `app.js` and `preview.js` with detailed comments.
- Skeleton loader, responsive layout, spinner behaviour.
- Comprehensive `README.md`, `.gitignore`, and documented source files.

### Changed
- `main.py` now only contains minimal Flask routes.
- HTML template simplified to rely on external JS.

### Removed
- Inline JavaScript previously embedded in `index.html`.

---

## [1.0.0] - 2025-08-14
### Added
- Initial Flask app with image upload and prompt form.
- Basic CSS styling and instant preview functionality.
- Azure OpenAI integration (image generation / edit endpoint).
