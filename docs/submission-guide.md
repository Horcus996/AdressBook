# Frontend / Backend Division and GitHub Submission Guide

> This guide splits the project files by **backend** and **frontend** roles into concrete files per member: 3 code files each. It also provides the branch plan, commit sequence, Git commands and pre-commit self-check. Shared documents are maintained by both members and are not counted in the 3 personal files.

## 1. File Ownership Summary

### 1.1 Frontend Member (Member A) — 3 Code Files

| # | File Path | Responsibility | Related Score |
|---|---|---|---|
| 1 | `address-book/templates/index.html` | Page structure: header statistics, toolbar (tabs / search / buttons), contact card container, add-edit modal, toast bar; semantic markup | Page style 10 |
| 2 | `address-book/static/css/style.css` | Visual styles: color variables, responsive card grid, buttons / chips / modal / toast layout and interaction states | Page style 10 |
| 3 | `address-book/static/js/app.js` | Frontend logic: contact rendering, bookmark toggle, filtering and search, modal form and dynamic method rows, CRUD calls, Excel import/export integration, toast feedback | Bookmark, multiple methods, import/export UI interaction |

### 1.2 Backend Member (Member B) — 3 Code Files

| # | File Path | Responsibility | Related Score |
|---|---|---|---|
| 1 | `address-book/app.py` | Flask application: contact data model, CRUD endpoints, bookmark toggle, validation and cleaning, JSON persistence, Excel import/export, template download | Bookmark 25, multiple methods 10, Excel import/export 25 |
| 2 | `address-book/requirements.txt` | Python dependency list (Flask, openpyxl) so others can reproduce the install | Reproducibility |
| 3 | `address-book/tests/smoke_test.py` | Backend smoke test: health check, create, favorite filter, bookmark toggle, update, export header and row count, import parsing, field validation, export round-trip, delete | Correctness, verifiability |

### 1.3 Shared Documents (Committed by Both)

| File Path | Description |
|---|---|
| `address-book/README.md` | Project overview, run steps, API reference (completed jointly) |
| `address-book/CODE_STANDARDS.md` | Team code standards, linked in the blog |
| `address-book/sample_contacts.xlsx` | Sample export file that can be reused for import demo |
| `docs/team-guide.md` | Collaboration workflow, blog template, PSP tables, deployment and self-check checklist |
| `docs/blog-draft.md` | Personal blog draft (each member publishes one) |

## 2. Frontend-Backend API Agreement (Integration Reference)

The frontend `app.js` talks to the backend `app.py` only through the endpoints below, exchanging JSON. Fields follow the backend data model:

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | Return the frontend page |
| GET | `/api/health` | Health check, returns contact count |
| GET | `/api/contacts` | List; optional `?favorite=1`, `?q=keyword` |
| POST | `/api/contacts` | Create a contact |
| PUT | `/api/contacts/<id>` | Update a contact |
| DELETE | `/api/contacts/<id>` | Delete a contact |
| POST | `/api/contacts/<id>/bookmark` | Toggle bookmark state |
| GET | `/api/export-contacts.xlsx` | Export all contacts |
| GET | `/api/template.xlsx` | Download the import template |
| POST | `/api/import` | Upload a `.xlsx` to import contacts |

Contact fields (identical on both sides): `id`, `name`, `bookmarked`, `phones[]`, `emails[]`, `socials[]`, `address`, `note`.

## 3. Suggested Commit Sequence (At Least 3 Commits Per Member)

Commit messages follow section 2 of `CODE_STANDARDS.md`: `type: short English description`. The sequence below is a reference; merge or split according to the actual implementation, but each member must have multiple traceable commits.

### 3.1 Backend Member (Member B) Commits

1. `feat: scaffold Flask app with contact model and JSON persistence`
   — commit the `app.py` skeleton, data model and local JSON read/write.
2. `feat: add contact CRUD and bookmark toggle endpoints`
   — commit contact CRUD and bookmark toggle endpoints, payload validation and cleaning.
3. `feat: implement Excel import and export with header aliases`
   — commit workbook building, export, template download and import parsing.
4. `test: cover CRUD, bookmark and Excel round-trip in smoke test`
   — commit `tests/smoke_test.py`.
5. `chore: pin Flask and openpyxl dependencies`
   — commit `requirements.txt`.

### 3.2 Frontend Member (Member A) Commits

1. `feat: build contact list layout and toolbar structure`
   — commit the `templates/index.html` page structure.
2. `style: add responsive card layout, modal and toast theme`
   — commit the `static/css/style.css` styles.
3. `feat: implement contact form and dynamic method rows`
   — commit the modal form and dynamic phone / email / social row logic in `app.js`.
4. `feat: connect UI to contact REST and Excel import/export APIs`
   — commit rendering, bookmark toggle, filter/search, import/export integration and feedback.

## 4. Git Operation Steps

> On this machine Git is installed at `C:\Program Files\Git\cmd\git.exe` (if it is not on PATH, use the full path or add that directory to the system PATH environment variable). The commands below use `git` as shorthand.

### 4.1 First Clone and Configuration

```bash
# Clone the team repository
git clone <team-repository-url>
cd <repository-directory>

# Confirm commit identity (each member configures their own GitHub account)
git config user.name  "your-github-username"
git config user.email "your-github-email"
```

### 4.2 Work on a Feature Branch

```bash
# Branch off main (backend example feature/backend-api, frontend example feature/frontend-ui)
git checkout -b feature/backend-api

# Stage and commit after coding (one thing per commit)
git add app.py
git commit -m "feat: add contact CRUD and bookmark toggle endpoints"

# Push the branch to the remote
git push -u origin feature/backend-api
```

### 4.3 Merge, Release and PR

1. On GitHub, open a **Pull Request** from the feature branch to `main`; the other member reviews it and merges after the smoke test passes.
2. After merging, go to **Releases → Draft a new release** and cut a version number (for example `v1.0.0`).
3. The blog includes the repository URL, standards document link, and PR / Release links.

### 4.4 Syncing the Teammate's Latest Code

```bash
git checkout main
git pull origin main
git checkout -b feature/<your-next-branch>
```

## 5. Pre-commit Self-check

### 5.1 Backend Member (Member B)

- [ ] `python tests/smoke_test.py` fully passes.
- [ ] Endpoint errors return JSON `{"error": ...}` with the correct status code (400 / 404).
- [ ] External input (request body, Excel cells) goes through cleaning and validation.
- [ ] Paths are derived from `Path(__file__).resolve().parent`; no hardcoded personal paths.
- [ ] Dependency changes are reflected in `requirements.txt`.
- [ ] No debug leftovers (temporary `print`, commented-out dead code).

### 5.2 Frontend Member (Member A)

- [ ] The page opens in the browser without console errors and API calls work.
- [ ] Form fields match the backend data model (multi-value fields are arrays).
- [ ] User input is escaped before rendering; no HTML injection risk.
- [ ] Styles use CSS variables; no scattered inline styles; feedback uses toast, not a bare `alert`.
- [ ] Import/export always goes through backend endpoints; the frontend does not assemble Excel directly.

## 6. Mapping to the Blog Record

- Fill the blog "Division of Labor" section according to the roles and files in section 1.
- The per-member commit counts in "Git Contribution Record" must match the section 3 commit sequence and the actual remote repository record.
- The contribution ratio is agreed by both members based on actual workload, totaling exactly 100%, consistent with commit records and division of labor.
