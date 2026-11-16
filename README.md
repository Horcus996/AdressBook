# Address Book Application

**Course:** EE308FZ Software Engineering (2601_FZU-MU_SE)
**Assignment:** Extreme Programming — Address Book Application
**Deadline:** 2026-11-17 23:59 (Beijing Time)

A web-based address book application built with Python 3 + Flask and plain HTML / CSS / JavaScript. It supports contact CRUD, bookmarking, multiple contact methods per contact, and Excel (`.xlsx`) import and export. Data is stored in a local JSON file, so no database needs to be installed to run the project.

## Features

- **Bookmark contacts** — one-click star toggle, bookmark state persisted, Favorites filter page, highlighted star on cards.
- **Multiple contact methods** — each contact can hold multiple phone numbers, emails and social accounts, plus a postal address; the form supports dynamic add/remove rows.
- **Excel import and export** — one-click `.xlsx` export with a labeled header and one row per contact; upload a compatible `.xlsx` to import contacts, with header recognition, multi-value splitting and blank-row skipping.
- **Responsive interface** — card layout, search, All/Favorites filtering, modal forms and toast feedback.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3 + Flask |
| Excel processing | openpyxl |
| Frontend | Plain HTML / CSS / JavaScript |
| Persistence | Local JSON file (`address-book/data/contacts.json`, generated on first run, not committed) |

## Quick Start

```powershell
# Enter the application directory
cd address-book

# Install dependencies
python -m pip install -r requirements.txt

# Start the application
python app.py

# Open in the browser
# http://127.0.0.1:5000
```

Run the smoke test without a running server:

```powershell
python tests/smoke_test.py
```

All 13 checks pass when the final line reads `All smoke tests passed.`.

## Repository Layout

```
.
├── README.md                     # This document (homepage overview)
├── address-book/
│   ├── app.py                    # Backend: routes, data model, Excel import/export, persistence
│   ├── requirements.txt          # Python dependency list
│   ├── CODE_STANDARDS.md         # Team code standards
│   ├── README.md                 # Detailed implementation and run guide
│   ├── sample_contacts.xlsx      # Sample export file (reusable for import testing)
│   ├── data/                     # Local runtime data (not committed)
│   ├── templates/index.html      # Frontend page structure
│   ├── static/css/style.css      # Frontend styles
│   ├── static/js/app.js          # Frontend interaction and API calls
│   └── tests/smoke_test.py       # Smoke test: CRUD, bookmark, import/export and round-trip
└── docs/
    ├── team-guide.md             # Collaboration workflow, blog template, PSP tables, deployment guide
    ├── submission-guide.md       # Frontend/backend division and GitHub submission guide
    └── blog-draft.md             # Personal blog draft (each member publishes one)
```

## Documentation

- [Detailed application guide](address-book/README.md) — requirements mapping, data model, feature details, API reference and troubleshooting.
- [Code standards](address-book/CODE_STANDARDS.md) — naming, formatting, commit message and review conventions.
- [Team collaboration guide](docs/team-guide.md) — workflow, blog template, PSP tables and deployment steps.
- [Submission guide](docs/submission-guide.md) — role-based file ownership, commit sequence and Git commands.
- [Blog draft](docs/blog-draft.md) — required blog sections and PSP tables to complete before publishing.

## API Reference (Summary)

| Method | Path | Description |
|---|---|---|
| GET | `/` | Frontend page |
| GET | `/api/health` | Health check, returns the contact count |
| GET | `/api/contacts` | Contact list; optional `?favorite=1`, `?q=keyword` |
| POST | `/api/contacts` | Create a contact |
| PUT | `/api/contacts/<id>` | Update a contact |
| DELETE | `/api/contacts/<id>` | Delete a contact |
| POST | `/api/contacts/<id>/bookmark` | Toggle bookmark state |
| GET | `/api/export-contacts.xlsx` | Export all contacts |
| GET | `/api/template.xlsx` | Download the import template |
| POST | `/api/import` | Upload a `.xlsx` to import contacts |

The full description of each endpoint is in the [detailed guide](address-book/README.md#9-api-reference).
