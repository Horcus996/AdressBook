# EE308FZ Extreme Programming — Address Book Assignment Blog (Draft)

> **Usage note:** items marked `[…]` need to be filled in by you and your teammate. After uploading screenshots and videos to CSDN, paste their links in the corresponding place. The two members may share this draft, but **each must publish an independent blog**. Check the "Pre-publish checklist" at the end before publishing.

## TOC

- [1. Assignment Information](#1-assignment-information)
- [2. Project Links](#2-project-links)
- [3. Git Contribution Record](#3-git-contribution-record)
- [4. Implementation Design](#4-implementation-design)
- [5. Running Evidence](#5-running-evidence)
- [6. Division of Labor](#6-division-of-labor)
- [7. Contribution Ratio](#7-contribution-ratio)
- [8. Collaboration Problems and Solutions](#8-collaboration-problems-and-solutions)
- [9. PSP Tables](#9-psp-tables)

---

## 1. Assignment Information

| Item | Content |
|---|---|
| Course for This Assignment | 2601_FZU-MU_SE |
| Team Name | [team name, to fill in] |
| Assignment Requirements | [assignment post link; insert the new post URL here after publishing] |
| Objectives of This Assignment | Implement the address book features and practice pair collaboration, Git and software engineering |
| Other References | [relevant materials, such as Flask documentation, openpyxl documentation, Python tutorials] |

## 2. Project Links

- GitHub team repository: [repository URL, to fill in]
- Code standards document: [raw link to CODE_STANDARDS.md in the repository, to fill in]
- Public application URL (if deployed): [public link; write N/A if not deployed]
- Pull Request: [PR link, to fill in]
- Release version: [Release link, to fill in]

## 3. Git Contribution Record

> Take the screenshot from the GitHub repository **Insights → Contributors** or the commit history page, showing each member's commit count.

Commit history screenshot:

![GitHub commit history]([screenshot link, to upload])

| Member | Commits |
|---|---:|
| Member A: [name / student ID] | [X] |
| Member B: [name / student ID] | [Y] |

> Requirement: at least 3 commits total, and both members must have meaningful coding records; the screenshot must let the teacher verify the commit authors.

## 4. Implementation Design

### 4.1 Technology Stack and Overall Structure

- **Backend:** Python 3 + Flask, providing REST-style endpoints for validation, business logic and Excel read/write.
- **Excel processing:** openpyxl, reading and writing `.xlsx` files with headers, column widths and cell content.
- **Frontend:** plain HTML / CSS / JavaScript, no build step required, so the page runs directly in the browser.
- **Persistence:** local JSON file (`data/contacts.json`); sample data is generated on first launch. No database is needed at course-demo scale.

The system has three layers: browser page → Flask endpoints → local data file. Frontend and backend exchange JSON, and the contact fields are consistent on both sides.

### 4.2 Bookmark Contacts

1. The data model adds a `bookmarked` boolean field to each contact, persisted to JSON so the state survives restarts.
2. The backend provides `POST /api/contacts/<id>/bookmark` to toggle between bookmarked and not bookmarked.
3. The list endpoint supports `?favorite=1` to return only bookmarked contacts for the Favorites filter page.
4. On the card, a star button shows the state: gold filled star `★` when bookmarked, gray hollow star `☆` otherwise; clicking it calls the toggle endpoint and refreshes the list. The header statistics show the total and favorite counts in real time.

### 4.3 Multiple Contact Methods

1. `phones`, `emails` and `socials` are string arrays, naturally supporting multiple records per field; `address` is a single text value.
2. In the add/edit modal, each method group is a set of dynamic input rows: click "+ Add …" to add a row, click the row-end `✕` to remove it; on save, all non-empty entries are collected.
3. The backend cleans values before saving: trims spaces and filters empty entries; imported data goes through the same cleaning.
4. On the card, information is grouped under Phone / Email / Social as chips; the address appears on its own line.

### 4.4 Excel Import and Export

**Export format:** the first row is a labeled header, one contact per row, multiple values separated by semicolons. Columns in order: `Name`, `Bookmarked`, `Phones`, `Emails`, `Social Accounts`, `Address`, `Note`.

- **Export flow:** the backend creates a workbook with openpyxl → writes the header → appends one row per contact → adjusts column widths → downloads `contacts.xlsx` through the browser.
- **Import flow:** upload a `.xlsx`, read the active worksheet → map the header row to canonical fields through an alias table (recognizing common English names) → parse rows one by one: rows without a name are skipped; multi-value cells are split on semicolons / commas; bookmark marks are parsed to booleans → append parsed contacts and save to local JSON.
- **Fault tolerance:** a clear error message appears when the file cannot be read; blank rows are ignored; a corrupted local data file falls back to sample data instead of crashing. The page also provides a blank template download to keep the import format consistent.

## 5. Running Evidence

> Record the following screenshots and video while running the application locally; the video must continuously show the real running application.

- Main interface screenshot (contact cards, stars, statistics): ![main interface]([screenshot link, to upload])
- Add / edit contact modal (multiple phones / emails / social accounts): ![modal]([screenshot link, to upload])
- Favorites filter page: ![favorites filter]([screenshot link, to upload])
- Exported Excel spreadsheet screenshot (header + one row per contact): ![exported Excel]([screenshot link, to upload])
- Import success result screenshot: ![import result]([screenshot link, to upload])
- **Complete demo video:** [video link, to upload to CSDN / Bilibili / another platform]

Suggested video order: launch the application → add a contact with multiple methods → bookmark / unbookmark → switch to Favorites filter → export and open the Excel file → import an Excel file → edit and delete a contact. Duration 2–5 minutes.

## 6. Division of Labor

| Member | Main Responsibilities | Modules |
|---|---|---|
| Member A: [name / student ID] | Backend data model, CRUD endpoints, Excel import/export, smoke tests | `app.py`, `tests/smoke_test.py` |
| Member B: [name / student ID] | Frontend layout, form interaction, bookmark and filtering, styles and feedback | `templates/index.html`, `static/css/style.css`, `static/js/app.js` |
| Shared | Requirements discussion, API and field agreement, code review, documentation and evidence | Repository documentation, blog material |

> Both members participated in coding. Even with a backend / frontend lean, each side has commits in the other's modules (integration adjustments, review fixes, etc.).

## 7. Contribution Ratio

| Member | Contribution Ratio |
|---|---:|
| Member A: [name / student ID] | [__]% |
| Member B: [name / student ID] | [__]% |
| **Total** | **100%** |

> The ratio must match the actual division of labor and Git commit records; the two percentages add up to exactly 100%.

## 8. Collaboration Problems and Solutions

| Problem | Solution | Owner |
|---|---|---|
| Frontend/backend disagreed on multi-value format (string vs array) | Agreed to use arrays and clean empty values / spaces before saving | [Member A / B] |
| Excel headers used different languages | Built a header alias mapping in the backend for common English and Chinese names | [Member A / B] |
| Local port 5000 was occupied | Closed the occupying process or changed the port in `app.py` and restarted | [Member A / B] |
| Merge conflicts between branches | Merged through Pull Request after review; resolved conflicts file by file together | [Member A / B] |
| [add other problems you actually encountered] | [corresponding solution] | [Member] |

## 9. PSP Tables

> PSP (Personal Software Process) records planned / actual time and defects for each phase; time is in minutes. Fill one table per member; record 0 for no defects, do not leave cells blank.

### 9.1 Member A: [name / student ID]

| Phase | Planned Time (min) | Actual Time (min) | Defects Injected | Defects Removed |
|---|---:|---:|---:|---:|
| Planning |  |  |  |  |
| Requirements Analysis |  |  |  |  |
| Design |  |  |  |  |
| Coding |  |  |  |  |
| Testing |  |  |  |  |
| Postmortem |  |  |  |  |
| **Total** |  |  |  |  |

### 9.2 Member B: [name / student ID]

| Phase | Planned Time (min) | Actual Time (min) | Defects Injected | Defects Removed |
|---|---:|---:|---:|---:|
| Planning |  |  |  |  |
| Requirements Analysis |  |  |  |  |
| Design |  |  |  |  |
| Coding |  |  |  |  |
| Testing |  |  |  |  |
| Postmortem |  |  |  |  |
| **Total** |  |  |  |  |

---

## Pre-publish Checklist

- [ ] Info table, TOC and project links are present and open correctly
- [ ] Commit history screenshot uploaded and both members' commit counts filled in
- [ ] Implementation design matches the code
- [ ] Screenshots and demo video links are accessible
- [ ] Division of labor is clear; contribution ratio totals 100%
- [ ] Both PSP tables are complete
- [ ] Repository permissions are visible to the teacher; the individual blog is published in the course community and its link submitted
