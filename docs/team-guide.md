# Team Collaboration and Submission Guide — Address Book Assignment

**Course:** EE308FZ Software Engineering (2601_FZU-MU_SE)
**Assignment:** Extreme Programming — Address Book Application
**Deadline:** 2026-11-17 23:59 (Beijing Time)

This guide is written for the two-person team. It covers the full workflow: division of labor, Git collaboration, feature development, evidence collection, CSDN blog writing, PSP recording, cloud deployment and the final self-check. Code and run instructions are in `../address-book/README.md`; code standards are in `../address-book/CODE_STANDARDS.md`.

---

## 1. Assignment Overview: What to Deliver

| # | Deliverable | Key Requirements |
|---|---|---|
| 1 | GitHub team repository | Upload all source code and documentation; at least 3 commits; both members have meaningful coding records |
| 2 | Feature implementation | Bookmark, multiple contact methods, Excel import/export; usable interface, runs correctly |
| 3 | Release and merge | Release a project version and open a Pull Request |
| 4 | Individual CSDN blog | Each member publishes one blog; a shared Markdown draft is allowed, but each must publish their own |
| 5 | Blog evidence | Info table, project links, commit history screenshots and per-member counts, implementation ideas, running screenshots, complete demo video, division of labor, contribution ratio, collaboration problems and solutions, one PSP table per member |
| 6 | Blog link submission | Submit the link to your own published blog through the course assignment channel |
| 7 | Optional bonus | A publicly accessible cloud deployment link (`localhost` does not count), up to +15 |

## 2. Recommended Schedule (Working Backwards)

CSDN blogs may require a review period after publication, so publish early; do not leave it to the last hour.

| Time | Task | Output |
|---|---|---|
| Evening 11-15 | Create the team repository, agree on code standards, discuss module boundaries and division of labor; get the code running locally | Repository, standards document, runnable skeleton |
| Morning 11-16 | Complete assigned modules on feature branches; commit continuously and review each other | Feature branches, multiple commits |
| Afternoon 11-16 | Integrate and test: import/export, bookmark, multiple methods; pass the smoke test; record screenshots and video | Demo-ready application |
| Morning 11-17 | Organize evidence, write the blog draft, fill PSP tables; open PR, cut Release | PR, Release, blog draft |
| Afternoon 11-17 | Each publishes the blog, checks links and repository permissions, submits the link; leave review buffer | Final submitted assignment |

## 3. Git and Team Repository Workflow

### 3.1 Initialize the Repository

1. **Fork** the provided assignment repository to your own GitHub account, then build the **two-person team repository** on that basis (one member owns the repository and adds the other as a Collaborator).
2. Both members clone the team repository locally:

```bash
git clone <team-repository-url>
cd address-book
```

3. Confirm the default branch is `main`; do not commit directly to `main` afterward.

### 3.2 Branch and Commit Conventions

- Branch names: `feature/<feature>`, `fix/<issue>`, `docs/<doc>` (details in section 1 of `CODE_STANDARDS.md`).
- Commit messages follow the `type: description` format, for example `feat: add bookmark toggle`.
- Each commit does one thing; run the smoke test locally before pushing.

Typical cycle:

```bash
git checkout -b feature/import-export
# code ...
git add .
git commit -m "feat: support xlsx import with header alias mapping"
git push origin feature/import-export
```

### 3.3 Merge, Release and PR

1. On GitHub, open a **Pull Request** from the feature branch to `main`; the other member reviews and merges it.
2. After merging, go to **Releases → Draft a new release**, set a version number (for example `v1.0.0`) and write release notes.
3. The blog includes the repository URL, the standards document URL, and the Release / PR links.

### 3.4 Commit Record Requirements

- At least **3 commits** in the repository total; at least 3 per member is recommended to keep the record balanced.
- Both students must write code; one person cannot do it all. The division of labor in the blog must match the commit records.
- Prepare screenshots from the GitHub repository **Insights → Contributors** or the commit history list, showing each member's commit count.

## 4. Suggested Division of Labor

The assignment requires both students to participate in development. The table below is a reference split and can be adjusted to the actual situation. The principle is that both sides touch frontend and backend, documentation and testing have an owner, and contributions are traceable.

| Role | Main Responsibilities | Modules |
|---|---|---|
| Member A (backend-leaning) | Data model, CRUD endpoints, Excel import/export, persistence and testing | `app.py`, `tests/smoke_test.py` |
| Member B (frontend-leaning) | Page layout, form interaction, bookmark and filtering, styles and feedback | `templates/index.html`, `static/css/style.css`, `static/js/app.js` |
| Shared | Requirements discussion, API and field agreement, code review, documentation and evidence | Repository documentation, blog material |

> Even if the lean is backend or frontend, both members should have commits in the other side's modules (for example, small fixes after review, integration adjustments) to satisfy the "both students must code" requirement.

## 5. Applying XP Practices

Following the basic XP rhythm, this project proceeds in this order:

1. **Plan:** discuss module boundaries (backend APIs, frontend pages, data model) and divide labor before writing any code.
2. **Code:** implement on the agreed API and data model; multi-value fields and error formats stay consistent across frontend and backend.
3. **Integrate:** before merging feature branches, integrate and test locally so import/export, bookmark and multiple methods all work together.
4. **Feedback:** check the result with the smoke test and a live demo; record discovered problems in the blog's "collaboration problems and solutions" section.

## 6. Evidence Collection Checklist

Keep the following material during development and integration so it can be used directly when writing the blog.

### 6.1 Git Evidence

- [ ] Screenshot of the repository home / commit history showing the full record
- [ ] Each member's commit count (counted from the Contributors page or commit list)
- [ ] Pull Request link and merge record
- [ ] Release version link

### 6.2 Running Evidence

- [ ] Main interface screenshot (contact cards, bookmark stars, statistics)
- [ ] Add / edit contact modal screenshot (multiple phones / emails / social accounts)
- [ ] Favorites filter page screenshot
- [ ] Screenshot of the exported `contacts.xlsx` opened in a spreadsheet (header + one row per contact)
- [ ] Screenshot of a successful import result / message
- [ ] **Complete demo video:** starting from launching the application, show adding a contact, registering multiple methods, bookmarking and unbookmarking, Favorites filtering, exporting and opening Excel, importing an Excel file, editing and deleting. The video must continuously show the real running application. 2–5 minutes is recommended; upload to CSDN / Bilibili / another video platform and put the link in the blog.

### 6.3 Other Material

- [ ] Code standards document link
- [ ] (If deployed) public access link and page screenshot
- [ ] PSP tables for both members

## 7. CSDN Blog Writing Guide

### 7.1 Required Content (Checked Against the Assignment)

1. **Assignment information and table of contents:** opening info table + Markdown TOC.
2. **Project links:** GitHub repository URL, code standards document URL, public application URL (if deployed), other relevant links.
3. **Git contribution evidence:** commit history screenshot + each member's commit count.
4. **Implementation design:** the ideas and methods used to implement each feature.
5. **Program evidence:** running screenshots + complete demo video.
6. **Division of labor:** clear responsibilities of each member.
7. **Contribution ratio:** the two percentages add up to **100%**.
8. **Collaboration problems and solutions:** problems each member encountered and how they were resolved.
9. **PSP tables:** one per member.

### 7.2 Opening Info Table (Required Format)

```markdown
| Item | Content |
|---|---|
| Course for This Assignment | 2601_FZU-MU_SE |
| Team Name | Your team name |
| Assignment Requirements | Link to the assignment post (insert the new post URL after publication) |
| Objectives of This Assignment | Implement the address book features and practice pair collaboration, Git and software engineering |
| Other References | Relevant materials and references |
```

### 7.3 Blog Markdown Skeleton

```markdown
# EE308FZ Extreme Programming — Address Book

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

## 1. Assignment Information
| Item | Content |
|---|---|
| Course for This Assignment | 2601_FZU-MU_SE |
| Team Name | ... |
| Assignment Requirements | ... |
| Objectives of This Assignment | ... |
| Other References | ... |

## 2. Project Links
- GitHub repository: ...
- Code standards document: ...
- Public application (if deployed): ...
- Release / PR: ...

## 3. Git Contribution Record
(commit history screenshot)
- Member A: X commits
- Member B: Y commits

## 4. Implementation Design
### 4.1 Bookmark Contacts
### 4.2 Multiple Contact Methods
### 4.3 Excel Import and Export

## 5. Running Evidence
(screenshots + demo video link)

## 6. Division of Labor
## 7. Contribution Ratio
| Member | Contribution Ratio |
|---|---|
| Member A | 55% |
| Member B | 45% |
| Total | 100% |

## 8. Collaboration Problems and Solutions
## 9. PSP Tables
### PSP Table for Member A
### PSP Table for Member B
```

### 7.4 Writing Notes

- The two members may share one Markdown draft, but **each publishes an independent blog**; put your own name / student ID in the title.
- Links must be accessible: keep the repository public or grant the teacher access; re-check that images display after upload.
- The contribution ratio must match the actual division of labor and commit records, totaling exactly 100%.
- "Collaboration problems and solutions" should describe the real process, for example mismatched frontend/backend fields, Excel header recognition, port occupation, merge conflicts, and the corresponding fixes.

## 8. PSP Table Templates

PSP (Personal Software Process) records planned and actual time and defects for each phase. The two templates below correspond to the two members; copy them into section 9 of the blog and fill in. Time is in minutes.

### 8.1 PSP Table for Member A

| Phase | Planned Time (min) | Actual Time (min) | Defects Injected | Defects Removed |
|---|---:|---:|---:|---:|
| Planning |  |  |  |  |
| Requirements Analysis |  |  |  |  |
| Design |  |  |  |  |
| Coding |  |  |  |  |
| Testing |  |  |  |  |
| Postmortem |  |  |  |  |
| **Total** |  |  |  |  |

### 8.2 PSP Table for Member B

| Phase | Planned Time (min) | Actual Time (min) | Defects Injected | Defects Removed |
|---|---:|---:|---:|---:|
| Planning |  |  |  |  |
| Requirements Analysis |  |  |  |  |
| Design |  |  |  |  |
| Coding |  |  |  |  |
| Testing |  |  |  |  |
| Postmortem |  |  |  |  |
| **Total** |  |  |  |  |

> Filling note: Defects Injected is the number of defects newly introduced in that phase; Defects Removed is the number found and fixed in that phase. Record 0 when there are no defects; do not leave cells blank.

## 9. Optional Bonus: Public Cloud Deployment Guide

> Do this only after the base requirements are complete. **Only a publicly accessible link counts as deployment; `http://localhost:5000` does not earn points.**

### 9.1 Preparation

1. Get a cloud server (Huawei Cloud or Alibaba Cloud lightweight application server both work) and obtain a public IP.
2. Open the application port (for example 5000, or 80) in the console security group / firewall.
3. Install Python 3.10+ and pip on the server.

### 9.2 Deployment Steps (Linux Server)

```bash
# 1. Clone the repository (or upload the source code)
git clone <team-repository-url>
cd <repository-directory>/address-book

# 2. Install dependencies
python3 -m pip install -r requirements.txt
python3 -m pip install gunicorn

# 3. Start in the background (gunicorn is recommended for production)
gunicorn -b 0.0.0.0:5000 app:app --daemon

# 4. Open in the browser
#    http://<server-public-ip>:5000
```

### 9.3 Notes

- If you use a domain name, ports 80 / 443 usually require ICP filing in China; for the assignment demo, `IP:port` is enough.
- Confirm that both the cloud provider firewall and the server internal firewall (such as `firewalld` / `ufw`) allow the port.
- After deployment, put the public link in the blog and screenshot a successful visit from another device.
- If the process stops, check the gunicorn / application logs; for a course demo you can also run `nohup python3 app.py &` temporarily.

## 10. Final Pre-submission Checklist

Check each item against the original assignment checklist:

- [ ] Forked the provided repository and discussed Git collaboration, code standards and division of labor with the teammate
- [ ] Bookmark feature implemented (25 points)
- [ ] Multiple contact methods implemented (10 points)
- [ ] Excel export implemented: labeled header, one row per contact (25 points)
- [ ] Excel import implemented: compatible format reads correctly (25 points)
- [ ] Interface usable and application runs correctly locally (page style 10 points)
- [ ] (Optional) Deployed to a public cloud server with an accessible link (+15)
- [ ] Project Release published and Pull Request opened
- [ ] Source code and related documentation uploaded to the GitHub team repository
- [ ] Blog contains: info table, TOC, project links, commit history screenshots and per-member counts, implementation design, screenshots and complete demo video, division of labor, contribution ratio (total 100%), collaboration problems and solutions, one PSP table per member
- [ ] Individual CSDN blog published in the course community and blog link submitted through the channel
- [ ] All links, images, videos and repository permissions re-checked so the teacher can verify
- [ ] Submitted before the deadline (11-17 23:59 Beijing Time), leaving time for blog review

## 11. Grading Criteria Self-check

| Criterion | Points | Self-check Focus |
|---|---:|---|
| Blog Markdown formatting; correct repository and standards links | 10 | TOC, info table, links open |
| Implementation ideas, screenshots, division of labor | 20 | Design described clearly, screenshots complete, division explicit |
| Page style | 10 | Clean layout, complete interaction feedback |
| Bookmark contacts | 25 | Star toggle, persisted state, Favorites filter work |
| Multiple contact methods | 10 | Multiple phones / emails / social accounts per contact |
| Excel import/export | 25 | Export format correct, import parsing correct |
| Cloud deployment (bonus) | +15 | Public link truly accessible |
