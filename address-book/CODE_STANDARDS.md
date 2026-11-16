# Code Standards — Address Book Project

> This document is the team code standards for the EE308FZ Software Engineering assignment. Both teammates agree to it before coding and follow it throughout development. The blog must link to this file in the repository.

## 1. Repository and Branch Rules

1. The team repository default branch is `main` and is protected: do not commit directly to `main`. All changes go through a feature branch and a Pull Request.
2. Branch naming:
   - New feature: `feature/<short-description>`, for example `feature/import-export`
   - Bug fix: `fix/<short-description>`, for example `fix/bookmark-toggle`
   - Documentation: `docs/<short-description>`
3. Each branch completes one clear goal; do not mix feature work, fixes and documentation in a single commit.
4. Before merging a Pull Request, the other member reviews it and confirms the smoke test passes.

## 2. Commit Message Standards

Commit messages use the format `type: description`, written in a short English imperative sentence with an initial capital letter, no more than 72 characters.

| Type | Purpose | Example |
|---|---|---|
| `feat` | New feature | `feat: add bookmark toggle on contact cards` |
| `fix` | Bug fix | `fix: trim empty phone numbers before saving` |
| `docs` | Documentation change | `docs: update README run steps` |
| `refactor` | Behavior-preserving refactor | `refactor: extract contact normalization helper` |
| `test` | Test related | `test: cover Excel import parsing` |
| `chore` | Build, dependencies, misc | `chore: pin openpyxl version` |

- One commit does one thing; before pushing, the code must run and the smoke test must pass.
- Both members must have traceable commit records. The repository has at least 3 commits total (at least 3 per member recommended).

## 3. Python Backend Standards

1. Follow PEP 8: 4-space indentation, UTF-8 encoding, prefer double-quoted strings.
2. Naming:
   - Functions and variables: `snake_case`, for example `normalize_contact_payload`
   - Constants: `UPPER_SNAKE_CASE`, for example `EXCEL_HEADERS`
   - Classes: `PascalCase`
3. Keep line width around 100 characters; split long expressions into intermediate variables.
4. Every public function has a one-line docstring explaining its purpose; complex helpers note their parameters.
5. Routes use plural nouns: `/api/contacts`, `/api/contacts/<id>`; HTTP verbs carry the semantics:
   - `GET` query, `POST` create, `PUT` update, `DELETE` delete.
6. Errors return JSON `{"error": "message"}` with the correct status code (400 bad request / 404 not found).
7. Do not hardcode personal paths; derive all paths from `Path(__file__).resolve().parent`.
8. External input (request body, Excel cells) must be cleaned and validated before entering the data model.

## 4. Frontend Standards (HTML / CSS / JavaScript)

1. Use semantic HTML: `<header>`, `<main>`, `<article>`, `<label>`, etc.; avoid overusing `<div>`.
2. JavaScript uses `camelCase` naming; event handlers start with `on`, for example `onSave`, `onImport`.
3. Design variables such as colors, spacing and radius live in the CSS `:root`; do not scatter inline styles.
4. Operation feedback (success, failure) uses the shared `toast` component, not a bare `alert`.
5. User input must be escaped before rendering to avoid HTML injection.
6. The frontend does not assemble Excel data directly; import and export always go through backend endpoints.

## 5. Data Model Convention

The Contact model always contains the following fields, consistent across frontend and backend:

| Field | Type | Description |
|---|---|---|
| `id` | integer | Unique id |
| `name` | string | Contact name, required |
| `bookmarked` | boolean | Whether bookmarked |
| `phones` | string[] | Phone number list, multiple allowed |
| `emails` | string[] | Email list, multiple allowed |
| `socials` | string[] | Social account list (WeChat / QQ / GitHub, etc.) |
| `address` | string | Postal address |
| `note` | string | Note |

- Multi-value fields always use arrays; strings joined only for display.
- Empty values are stored as empty strings or empty arrays; do not use `null` as a placeholder.

## 6. Testing and Pre-commit Checks

1. Before pushing, run `python tests/smoke_test.py` locally; it must fully pass before the work is done.
2. Before committing, remove debug leftovers (debug `print` statements, commented-out dead code, temporary files).
3. `data/contacts.json` is local runtime data and is not committed to the repository (already ignored in `.gitignore`).
4. When dependencies change, update `requirements.txt` so others can reproduce the install.

## 7. Collaboration Discipline

1. Discuss module boundaries and division of labor before coding (see `docs/team-guide.md`).
2. Both students must participate in coding; the work cannot be completed by one person alone. Commit records and the blog division of labor must match.
3. Resolve disagreements in a repository Issue or group chat, and write the conclusion back into the documentation; do not rely on verbal agreements.
