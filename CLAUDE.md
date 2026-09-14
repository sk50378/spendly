# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Spendly is a Flask-based expense tracker. This is a step-by-step learning project (see the comments in `app.py` and `database/db.py` referencing "Step 1", "Step 3", etc.) — much of the backend is intentionally left as stubs for incremental implementation, while the marketing/landing pages and auth-page UI are fully built out.

## Commands

Activate the existing virtualenv before running anything:

```bash
source venv/Scripts/activate   # Windows Git Bash
# or
source venv/bin/activate       # macOS/Linux
```

Run the dev server (Flask debug mode, port 5001):

```bash
python app.py
```

Install/update dependencies:

```bash
pip install -r requirements.txt
```

Testing: `pytest` and `pytest-flask` are listed in `requirements.txt`, but no test suite exists yet in the repo.

## Architecture

- **Single-file Flask app** (`app.py`) — all routes are defined directly on the module-level `app` object; no blueprints. Routes fall into two groups:
  - Implemented pages: `/`, `/register`, `/login`, `/terms`, `/privacy` — each just does `render_template(...)`.
  - Placeholder routes (explicitly commented "students will implement these"): `/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete` — these return plain strings like `"Add expense — coming in Step 7"` rather than real behavior. The `/register` and `/login` templates already POST to these routes, but the Flask routes are GET-only stubs — wiring up real POST handling is expected future work.
  - `app.run(debug=True, port=5001)` — the app always runs on **port 5001**, not Flask's default 5000.

- **Database layer is not yet implemented.** `database/db.py` is a stub with docstring-style comments describing the intended API (`get_db()`, `init_db()`, `seed_db()` using sqlite3), but no code exists there yet. `database/__init__.py` is empty. Don't assume any DB connection or schema currently exists — expense/user data on the implemented pages is all hardcoded mock data in the templates.

- **Templates** (`templates/`) all extend `base.html`, which defines the shared shell: nav bar, `<main>` content block, footer, and shared `<script>`/`<link>` tags. Page-specific content goes in `{% block content %}`; page titles in `{% block title %}`.

- **Styling** is a single hand-written stylesheet (`static/css/style.css`, no preprocessor/build step) driven by CSS custom properties defined in `:root` (colors like `--ink`, `--accent`, `--paper`; fonts `--font-display` / `--font-body`; radii). Match this token system rather than hardcoding new colors/fonts. Sections of the stylesheet are marked with `/* ---- Section name ---- */` banner comments — keep new rules grouped under an appropriately named banner rather than appended at the end.

- **JavaScript** is vanilla, no framework or bundler — all page behavior lives in `static/js/main.js`, loaded globally via `base.html`. Existing patterns wrap each independent feature (e.g. the landing page's video modal) in its own IIFE that no-ops via early `return` if its target elements aren't present on the current page, so the single global script file stays safe to include on every page.

- No `package.json`, no frontend build tooling — static assets are served as-is by Flask's `static/` folder via `url_for('static', filename=...)`.
