# Spec: Login and Logout

## Overview
This feature completes authentication for Spendly. `GET /login` and `login.html` already exist and render a complete sign-in form, but there is no backend logic behind it — the route only accepts `GET` and nothing verifies credentials or starts a session. `GET /logout` is still the Step 3 stub, returning a raw string. This step wires up `POST /login` to verify a submitted email/password against the `users` table (using `get_user_by_email`, added in Step 2) and, on success, starts a Flask session; it also implements `/logout` to clear that session. This is the step where `flask.session` is introduced to the app for the first time, so it also adds the `SECRET_KEY` Flask requires to sign session cookies. Building a visible profile or expense dashboard is out of scope — after login the user is redirected back to the landing page (`/`), where the navbar now shows the logged-in user's name in place of "Sign in", with `session['user_id']` and `session['user_name']` set.

## Depends on
- Step 1 — Database setup (`01-database-setup.md`): requires the `users` table and `get_db()`.
- Step 2 — Registration (`02-registration.md`): requires `get_user_by_email(email)` in `database/db.py` and at least one existing account (e.g. the seeded `demo@spendly.com` / `demo123` user) to log in with.

## Routes
- `POST /login` — accepts the sign-in form submission, verifies email/password, starts a session, then redirects — public
- `GET /login` — no behavior change, but the route decorator must add `methods=["GET", "POST"]` to also accept the POST above — public
- `GET /logout` — replaces the Step 3 stub; clears the session and redirects to `/login` — logged-in (safe to hit while logged out too; it just no-ops and redirects)

## Database changes
No new table, column, or constraint is needed — the existing `users` table and the `get_user_by_email(email)` helper from Step 2 already cover credential lookup for login. No new functions are needed in `database/db.py` for this step.

## Templates
- **Create:** none
- **Modify:**
  - `templates/login.html` — change the form's hardcoded `action="/login"` to `action="{{ url_for('login') }}"`
  - `templates/base.html` — the nav currently always shows "Sign in" / "Get started". Change it to check `session.get('user_id')`: when logged in, show the logged-in user's name (`session['user_name']`) in place of "Sign in", and a "Log out" link (`url_for('logout')`) in place of "Get started"; when logged out, keep the existing "Sign in" / "Get started" links. This is required so a logged-in user actually has a way to trigger `/logout` from the UI.

## Files to change
- `app.py` — set `app.secret_key` (required before `flask.session` can be used); update the `/login` route to accept `GET` and `POST`; on `POST`, read `request.form`, look up the user with `get_user_by_email`, verify the password with `check_password_hash`, and either re-render `login.html` with an `error` message or set `session['user_id']` / `session['user_name']` and `redirect(url_for('landing'))` on success; replace the `/logout` stub with a real implementation that clears the session and redirects to `/login`
- `templates/login.html` — fix hardcoded form action to use `url_for('login')`
- `templates/base.html` — make the nav session-aware (see Templates above)

## Files to create
No new files needed.

## New dependencies
No new dependencies. Password verification uses `werkzeug.security.check_password_hash`, from the same `werkzeug` package already used for hashing in Step 2.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterized queries only — never f-strings in SQL
- Passwords hashed with werkzeug — verify with `check_password_hash`, never compare plaintext passwords
- Use CSS variables — never hardcode hex values (no new CSS should be needed; reuse existing `.auth-error` / nav classes)
- All templates extend `base.html`
- Validate that `email` and `password` are non-blank server-side before querying the database
- On invalid credentials, show one generic error (e.g. "Invalid email or password") — never reveal whether the email exists or the password was wrong specifically, to avoid user enumeration
- Store only `session['user_id']` and `session['user_name']` in the session — never store the password or password_hash in the session
- `app.secret_key` must be set before any route uses `session`; do not commit a real production secret — a locally generated/dev value is fine at this stage
- On any validation or authentication failure, re-render `login.html` with `render_template("login.html", error=...)` — never a raw string return
- `/logout` must never return a raw string once implemented — it must clear the session and `redirect(url_for('login'))`
- On successful login, redirect using `url_for('landing')`, never a hardcoded path
- Do not implement the `/profile` page content — it stays the Step 4 stub; this step only adds `session['user_id']`/`session['user_name']`, it does not change or route through `/profile`
- Do not touch the `/expenses/*` stub routes

## Definition of done
- [ ] Submitting `/login` with the seeded demo account (`demo@spendly.com` / `demo123`) redirects to `/` (landing page) and a session cookie is set with `user_id` and `user_name`
- [ ] Submitting `/login` with a correct email but wrong password re-renders `login.html` with a generic error, without revealing which field was wrong
- [ ] Submitting `/login` with an email that doesn't exist re-renders `login.html` with the same generic error message (no user enumeration)
- [ ] Submitting `/login` with a blank email or blank password re-renders the form with a validation error instead of crashing
- [ ] Visiting `/logout` after logging in clears the session and redirects to `/login`
- [ ] Visiting `/logout` while already logged out does not crash and redirects to `/login`
- [ ] After logging in, the navbar shows the user's name in place of "Sign in" and a "Log out" link in place of "Get started"; after logging out, the navbar reverts to "Sign in" / "Get started"
- [ ] `GET /login`, `GET /register`, `GET /`, `GET /terms`, and `GET /privacy` still render correctly (no regression)
- [ ] The `/profile` and `/expenses/*` stub routes are otherwise unchanged
- [ ] Viewing the login page's HTML source shows the form's `action` attribute pointing at `/login` via `url_for()`, not a hardcoded string
