# Spec: Registration

## Overview
This feature completes account creation for Spendly. `GET /register` and `register.html` already exist and render a visually complete form, but there is no backend logic behind it: the route only accepts `GET`, and nothing validates input, hashes passwords, checks for duplicate emails, or writes to the `users` table. This step wires up `POST /register` so a visitor can actually create an account, building directly on the `users` schema from Step 1 (database setup). Login/session handling is intentionally out of scope here — after a successful registration a success message should shown there and then the user is redirected to `/login` to sign in, keeping this step focused on one responsibility: creating the account record.

## Depends on
- Step 1 — Database setup (`01-database-setup.md`): requires the `users` table (`id`, `name`, `email` UNIQUE NOT NULL, `password_hash`, `created_at`) and `get_db()` already implemented in `database/db.py`.

## Routes
- `POST /register` — accepts the registration form submission, validates input, hashes the password, creates the user, then redirects — public
- `GET /register` — no behavior change, but the route decorator must add `methods=["GET", "POST"]` to also accept the POST above — public

## Database changes
No new table, column, or constraint is needed — the existing `users` table (name, email, password_hash) already covers registration.

This step does add two new **functions** to `database/db.py` (helpers, not schema changes):
- `get_user_by_email(email)` — returns the matching row or `None`, used to check for duplicate emails before insert
- `create_user(name, email, password_hash)` — inserts a new row into `users` via a parameterized `INSERT` and returns the new user id

## Templates
- Create: none
- Modify:
  - `templates/register.html` — change the form's hardcoded `action="/register"` to `action="{{ url_for('register') }}"`; add `{% if error %}` block usage already present is reused to show validation/duplicate-email errors passed from the route

## Files to change
- `app.py` — update the `/register` route to accept `GET` and `POST`; on `POST`, read `request.form`, validate fields, call `get_user_by_email` / `create_user`, and either re-render `register.html` with an `error` message or `redirect(url_for('login'))` on success
- `database/db.py` — add `get_user_by_email(email)` and `create_user(name, email, password_hash)` functions, using parameterized queries and the existing `get_db()` connection helper
- `templates/register.html` — fix hardcoded form action to use `url_for('register')`

## Files to create
No new files needed.

## New Dependencies
No new dependencies. Password hashing uses `werkzeug.security.generate_password_hash`, already imported in `database/db.py` and already in `requirements.txt` via `werkzeug`.

## Rules to implementation
- No SQLAlchemy or ORMs
- Parameterized queries only — never f-strings in SQL
- Passwords hashed with werkzeug (`generate_password_hash`) — never store or log plaintext passwords
- Use CSS variables — never hardcode hex values (no new CSS should be needed; reuse the existing `.auth-error` class)
- All templates extend `base.html`
- Validate `name`, `email`, and `password` server-side even though the form has HTML5 `required` attributes — never trust client-side validation alone
- Enforce a minimum password length of 8 characters server-side, matching the form's placeholder text
- Check for an existing email via `get_user_by_email()` before inserting; on duplicate, re-render `register.html` with an `error` message instead of letting a `sqlite3.IntegrityError` bubble up
- On any validation failure, re-render `register.html` with `render_template("register.html", error=...)` — never a raw string return
- On success, redirect using `url_for('login')`, never a hardcoded path
- Do not add `flask.session` or login/auto-login logic in this step — that belongs to a future Login step
- Do not touch the `/logout`, `/profile`, or `/expenses/*` stub routes

## Definition of done
- [ ] Submitting the `/register` form with valid name, email, and an 8+ character password creates a new row in `users` with a hashed (not plaintext) password
- [ ] Submitting with an email that already exists (e.g. `demo@spendly.com`) does not create a duplicate row and re-renders `register.html` showing an error message
- [ ] Submitting with a blank name, blank email, or blank password re-renders the form with a validation error instead of crashing
- [ ] Submitting a password shorter than 8 characters re-renders the form with a validation error
- [ ] On successful registration, the browser is redirected to `/login`
- [ ] `GET /register`, `GET /login`, `GET /`, `GET /terms`, and `GET /privacy` still render correctly (no regression)
- [ ] The `/logout`, `/profile`, and `/expenses/*` stub routes are unchanged
- [ ] Viewing the register page's HTML source shows the form's `action` attribute pointing at `/register` via `url_for()`, not a hardcoded string
