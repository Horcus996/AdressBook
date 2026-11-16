# EE308FZ Extreme Programming — Address Book Application

## TOC

- [1. Assignment Information](#1-assignment-information)
- [2. Project Links](#2-project-links)
- [3. Git Contribution Record](#3-git-contribution-record)
- [4. Implementation Design](#4-implementation-design)
- [5. Program Evidence](#5-program-evidence)
- [6. Division of Labor](#6-division-of-labor)
- [7. Contribution Ratio](#7-contribution-ratio)
- [8. PSP Tables](#8-psp-tables)

---

## 1. Assignment Information

| Item | Content |
|---|---|
| Course for This Assignment | 2601_FZU-MU_SE |
| Team Name | Address Book Team |
| Assignment Requirements | https://bbs.csdn.net/topics/620593436 |
| Objectives of This Assignment | Implement the address book features and practice pair collaboration, Git and software engineering |
| Other References | Flask documentation, openpyxl documentation, Python 3 standard library tutorial |

## 2. Project Links

- GitHub team repository: https://github.com/Horcus996/AdressBook
- Code standards document: https://github.com/Horcus996/AdressBook/blob/main/address-book/CODE_STANDARDS.md
- Project overview (root README): https://github.com/Horcus996/AdressBook/blob/main/README.md
- Pull Request #1: https://github.com/Horcus996/AdressBook/pull/1
- Pull Request #2: https://github.com/Horcus996/AdressBook/pull/2
- Release version: https://github.com/Horcus996/AdressBook/releases/tag/v1.0.0

## 3. Git Contribution Record

> Screenshot taken from the GitHub repository **Insights → Contributors** or the commit history page, showing each member's commit count. The repository contains at least three commits, and both members have meaningful coding records.

Commit history screenshot:

![GitHub commit history](https://i-blog.csdnimg.cn/direct/a2ec0f6a789049e2846a11ec86a0ccdb.png#pic_center)

| Member | GitHub Username | Commits |
|---|---|---:|
| Member A: Wenjie Huang (832401206) | whichdogthree | 14 |
| Member B: Haodong Wu (832401221) | hodden2026 | 3 |

## 4. Implementation Design

### 4.1 Technology Stack and Overall Structure

| Layer | Technology | Rationale |
|---|---|---|
| Backend | Python 3 + Flask | Lightweight web framework with clear routes and fast startup; easy for pair collaboration |
| Excel processing | openpyxl | Standard Python library for reading and writing `.xlsx`, supporting headers, column widths and cell content |
| Frontend | Plain HTML / CSS / JavaScript | No build step required; the page runs directly in the browser with minimal environment dependencies |
| Persistence | Local JSON file (`data/contacts.json`) | Sufficient for course-demo scale; no database to install; sample data is generated on first launch |

The system has three layers: browser page → Flask endpoints → local data file. The frontend and backend exchange JSON, and the contact fields are consistent on both sides: `id`, `name`, `bookmarked`, `phones[]`, `emails[]`, `socials[]`, `address`, `note`.

### 4.2 Bookmark Contacts

**Goal:** mark frequent or important contacts as favorites so they are easy to recognize and reach quickly.

1. The data model adds a `bookmarked` boolean field to each contact, persisted to JSON so the state survives restarts.
2. The backend exposes `POST /api/contacts/<id>/bookmark`, which toggles the state between `true` and `false`.
3. The list endpoint supports `?favorite=1` to return only bookmarked contacts, used by the Favorites filter page.
4. On the card, a star button shows the state: a gold filled star `★` when bookmarked, a gray hollow star `☆` otherwise; clicking it calls the toggle endpoint and refreshes the list. The header statistics show the total contact count and the favorite count in real time.
5. When reading bookmark marks from Excel, only values such as `Yes`, `Y`, `True`, `1`, `bookmarked` and `favorite` count as bookmarked; any other value (including `No`, `0` or an empty string) is treated as unbookmarked.

### 4.3 Multiple Contact Methods

**Goal:** one contact can hold several pieces of contact information: phone numbers, emails, social accounts and a postal address.

1. `phones`, `emails` and `socials` are string arrays, which naturally support multiple records per field; `address` is a single text value.
2. In the add/edit modal, each of the three method groups is a set of dynamic input rows: click "+ Add …" to add a row, click the `✕` at the end of a row to remove it; on save, all non-empty entries are collected.
3. The backend cleans values before saving: trim surrounding spaces and filter out empty entries; imported data goes through the same cleaning.
4. On the card, information is grouped under Phone / Email / Social, each entry shown as a chip; the address is displayed on its own line.

### 4.4 Excel Import and Export

**Export format (`.xlsx`):** the first row is a labeled header; each contact occupies one row; multiple values inside a cell are separated by semicolons. Columns in order: `Name`, `Bookmarked`, `Phones`, `Emails`, `Social Accounts`, `Address`, `Note`.

- **Export flow:** the backend creates a workbook with openpyxl → writes the header → appends one row per contact → adjusts column widths → downloads `contacts.xlsx` through the browser.
- **Import flow:** upload a `.xlsx`, read the active worksheet → map the header row to canonical fields through an alias table that recognizes common English column names → parse rows one by one: rows without a name are skipped; multi-value cells are split on semicolons or commas; bookmark marks are parsed to booleans → append parsed contacts and save to local JSON.
- **Fault tolerance:** a clear error message appears when the file cannot be read; blank rows are ignored automatically; a corrupted local data file falls back to sample data instead of crashing. The page also provides a blank template download to keep the import format consistent.

### 4.5 Supporting Interactions

- **Search:** real-time fuzzy matching across name, phone, email, social account, address and note.
- **Filter:** switch between All and Favorites tabs.
- **CRUD:** create and edit through the modal form; delete asks for confirmation first.
- **Feedback:** success and failure messages appear through a bottom toast.

### 4.6 API Reference

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

## 5. Program Evidence

> Screenshots and the complete demonstration video are recorded while the application runs locally. The video continuously shows the real running application.

- Main interface (contact cards, stars, statistics):

![Main interface](https://i-blog.csdnimg.cn/direct/cbd685ef04d64cd49904ffe6609e0921.png)

- Add / edit contact modal (multiple phones / emails / social accounts):

![Add / edit contact modal](https://i-blog.csdnimg.cn/direct/9d802e7f850f4e09b10ff3b05524a451.png)

- Favorites filter page:

![Favorites filter](https://i-blog.csdnimg.cn/direct/de8faa340d144b299b4579141c8ec0e9.png)

- Exported Excel spreadsheet (header + one row per contact):

![Exported Excel](https://i-blog.csdnimg.cn/direct/3654206219004d8d92c51f2191d3ee09.png)

- Import success result:

![Import result](https://i-blog.csdnimg.cn/direct/165e8dcf0f23421d88e89f833ade5a4b.png)

- Complete demo video:

[video(video-KS9Px8rn-1794822807130)(type-csdn)(url-https://live.csdn.net/v/embed/553543)(image-https://v-blog.csdnimg.cn/asset/07356bb988e7780061ac0d6b74bcb0e2/cover/Cover0.jpg)(title-Address Book)]

The backend smoke test covers health check, sample data loading, create, favorite filter, bookmark toggle, update, string bookmark parsing, export header and row count, import parsing, imported field validation, export round-trip validity, and delete; all 15 checks pass locally.

## 6. Division of Labor

| Member | Main Responsibilities | Modules |
|---|---|---|
| Member A: Wenjie Huang (832401206) | Frontend layout, form interaction, bookmark and filtering, styles and feedback | `templates/index.html`, `static/css/style.css`, `static/js/app.js` |
| Member B: Haodong Wu (832401221) | Backend data model, CRUD endpoints, bookmark toggle, Excel import/export, smoke tests | `app.py`, `tests/smoke_test.py`, `requirements.txt` |
| Shared | Requirements discussion, API and field agreement, code review, documentation and evidence | Repository documentation, blog material |

Both members participated in coding and review; integration adjustments and fixes were committed through the backend feature branch and merged by Pull Request.

## 7. Contribution Ratio

| Member | Contribution Ratio |
|---|---:|
| Member A: Wenjie Huang (832401206) | 50% |
| Member B: Haodong Wu (832401221) | 50% |
| **Total** | **100%** |

## 8. PSP Tables

> PSP (Personal Software Process) records planned / actual time and defects for each phase; time is in minutes. One table per member; 0 means no defects.

### 8.1 Member A: Wenjie Huang (832401206)

| Phase | Planned Time (min) | Actual Time (min) | Defects Injected | Defects Removed |
|---|---:|---:|---:|---:|
| Planning | 30 | 25 | 0 | 0 |
| Requirements Analysis | 30 | 35 | 1 | 0 |
| Design | 40 | 45 | 1 | 1 |
| Coding | 120 | 150 | 3 | 2 |
| Testing | 40 | 35 | 1 | 3 |
| Postmortem | 15 | 15 | 0 | 1 |
| **Total** | **275** | **305** | **6** | **7** |

### 8.2 Member B: Haodong Wu (832401221)

| Phase | Planned Time (min) | Actual Time (min) | Defects Injected | Defects Removed |
|---|---:|---:|---:|---:|
| Planning | 30 | 25 | 0 | 0 |
| Requirements Analysis | 30 | 30 | 0 | 0 |
| Design | 40 | 40 | 1 | 0 |
| Coding | 120 | 140 | 2 | 1 |
| Testing | 40 | 40 | 1 | 2 |
| Postmortem | 15 | 15 | 0 | 1 |
| **Total** | **275** | **290** | **4** | **4** |
