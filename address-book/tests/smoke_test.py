
"""
Smoke test for the Address Book application.

Uses Flask's built-in test client (no real network port needed) and writes all
runtime data to a temporary directory, so the local demo data is untouched.

Run:
    python tests/smoke_test.py
"""

import io
import sys
import tempfile
from pathlib import Path

# Make the application package importable when the script is run directly.
APP_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(APP_DIR))

import app as address_book  # noqa: E402
from openpyxl import Workbook, load_workbook  # noqa: E402

# Redirect persistence to a temporary directory for the test run.
tmp_dir = Path(tempfile.mkdtemp())
address_book.DATA_DIR = tmp_dir
address_book.DATA_FILE = tmp_dir / "contacts.json"
address_book.contacts = address_book.load_contacts()

client = address_book.app.test_client()


def check(condition, message):
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}")


# 1. Health endpoint ---------------------------------------------------------
resp = client.get("/api/health")
check(resp.status_code == 200, "health endpoint returns 200")


# 2. Seed contacts are listed ------------------------------------------------
resp = client.get("/api/contacts")
seed_contacts = resp.get_json()
check(len(seed_contacts) >= 3, f"seed contacts loaded ({len(seed_contacts)})")


# 3. Create a contact with multiple contact methods -------------------------
payload = {
    "name": "Test Person",
    "bookmarked": True,
    "phones": ["130-0000-1111", "0591-1234567"],
    "emails": ["test@example.com"],
    "socials": ["WeChat: test_wx"],
    "address": "No. 9 Test Road",
    "note": "smoke test",
}

resp = client.post("/api/contacts", json=payload)
check(resp.status_code == 201, "create contact returns 201")
new_id = resp.get_json()["id"]


# 4. Bookmark filter shows the favorite contact ------------------------------
resp = client.get("/api/contacts?favorite=1")
favorites = resp.get_json()
check(
    any(c["id"] == new_id for c in favorites),
    "bookmarked contact appears in the Favorites filter",
)


# 5. Toggle bookmark off -----------------------------------------------------
resp = client.post(f"/api/contacts/{new_id}/bookmark")
body = resp.get_json()
check(
    resp.status_code == 200 and body["bookmarked"] is False,
    "bookmark toggle works",
)


# 6. Update contact -----------------------------------------------------------
resp = client.put(
    f"/api/contacts/{new_id}",
    json={**payload, "name": "Test Person Renamed"},
)
check(
    resp.status_code == 200 and resp.get_json()["name"] == "Test Person Renamed",
    "update contact works",
)


# Regression test: string "false" -------------------------------------------
resp = client.put(
    f"/api/contacts/{new_id}",
    json={**payload, "bookmarked": "false"},
)
check(
    resp.status_code == 200
    and resp.get_json()["bookmarked"] is False,
    "string false is parsed as an unbookmarked contact",
)


# Regression test: string "0" -----------------------------------------------
# Verify that the string "0" disables bookmarking.
resp = client.put(
    f"/api/contacts/{new_id}",
    json={**payload, "bookmarked": "0"},
)
check(
    resp.status_code == 200
    and resp.get_json()["bookmarked"] is False,
    "string zero is parsed as an unbookmarked contact",
)


# 7. Export to .xlsx: header + one row per contact ---------------------------
resp = client.get("/api/export-contacts.xlsx")
check(resp.status_code == 200, "export returns 200")

workbook = load_workbook(io.BytesIO(resp.data))
sheet = workbook.active
rows = list(sheet.iter_rows(values_only=True))

expected_header = (
    "Name",
    "Bookmarked",
    "Phones",
    "Emails",
    "Social Accounts",
    "Address",
    "Note",
)

check(
    tuple(rows[0]) == expected_header,
    "export header matches the required format",
)

check(
    len(rows) == len(seed_contacts) + 2,
    "one row per contact in the export (header + seed + created contact)",
)


# 8. Build a compatible .xlsx and import it ----------------------------------
import_wb = Workbook()
import_ws = import_wb.active

import_ws.append(list(expected_header))
import_ws.append(
    [
        "Imported User",
        "Yes",
        "131-2222-3333",
        "imp@example.com",
        "QQ: 999",
        "Import Road",
        "imported",
    ]
)

buffer = io.BytesIO()
import_wb.save(buffer)
buffer.seek(0)

resp = client.post(
    "/api/import",
    data={"file": (buffer, "import.xlsx")},
    content_type="multipart/form-data",
)

body = resp.get_json()
check(
    resp.status_code == 200 and body["imported"] == 1,
    "import parses one row",
)


# 9. Imported fields are parsed correctly ------------------------------------
resp = client.get("/api/contacts?q=Imported")
imported = resp.get_json()

check(
    len(imported) == 1
    and imported[0]["bookmarked"] is True
    and imported[0]["phones"] == ["131-2222-3333"],
    "imported name / bookmark / phone are parsed correctly",
)


# 10. Export after import still produces a valid workbook --------------------
resp = client.get("/api/export-contacts.xlsx")
load_workbook(io.BytesIO(resp.data))
check(True, "export after import opens as a valid .xlsx file")


# 11. Delete contact ---------------------------------------------------------
resp = client.delete(f"/api/contacts/{new_id}")
check(resp.status_code == 200, "delete contact works")


print("\nAll smoke tests passed.")