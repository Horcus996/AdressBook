"""
EE308FZ Software Engineering - Extreme Programming Assignment
Address Book Application (Flask + openpyxl)

Core features required by the assignment:
  1. Bookmark / favorite contacts                       (25 pts)
  2. Multiple contact methods per contact                (10 pts)
  3. Excel-based import / export (.xlsx)                 (25 pts)

Run locally:
    python -m pip install -r requirements.txt
    python app.py
    Open http://127.0.0.1:5000
"""

import json
import re
from io import BytesIO
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_file
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter

# --------------------------------------------------------------------------- #
# Paths and constants
# --------------------------------------------------------------------------- #
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "contacts.json"

# Column order used both for export and for the downloadable template.
EXCEL_HEADERS = [
    "Name",
    "Bookmarked",
    "Phones",
    "Emails",
    "Social Accounts",
    "Address",
    "Note",
]

# Acceptable header aliases when importing, mapped to the canonical field.
HEADER_ALIASES = {
    "name": ["name", "contact name"],
    "bookmarked": ["bookmarked", "favorite", "starred", "bookmark"],
    "phones": ["phones", "phone", "phone numbers", "telephone"],
    "emails": ["emails", "email", "email address"],
    "socials": ["social accounts", "social account", "socials", "social", "wechat"],
    "address": ["address", "postal address"],
    "note": ["note", "remark"],
}

BOOKMARK_TRUE_VALUES = {"yes", "y", "true", "1", "bookmarked", "favorite"}

# Sample contacts seeded on the very first run so the demo works out of the box.
SEED_CONTACTS = [
    {
        "id": 1,
        "name": "Alice Wang",
        "bookmarked": True,
        "phones": ["138-0000-0001", "0591-88880001"],
        "emails": ["alice.wang@example.com"],
        "socials": ["WeChat: alice_wx", "QQ: 100001"],
        "address": "No. 1 Gongye Road, Fuzhou, Fujian",
        "note": "Lab partner",
    },
    {
        "id": 2,
        "name": "Bob Chen",
        "bookmarked": False,
        "phones": ["139-1111-2222"],
        "emails": ["bob.chen@example.com", "bob@workmail.com"],
        "socials": ["GitHub: bobchen"],
        "address": "No. 2 Software Avenue, Fuzhou",
        "note": "",
    },
    {
        "id": 3,
        "name": "Carrie Lin",
        "bookmarked": True,
        "phones": ["137-3333-4444"],
        "emails": ["carrie.lin@example.com"],
        "socials": ["WeChat: carrie_l", "Instagram: carrie.lin"],
        "address": "No. 8 University Town, Minhou, Fuzhou",
        "note": "Group teammate",
    },
]

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


# --------------------------------------------------------------------------- #
# Persistence helpers
# --------------------------------------------------------------------------- #
def save_contacts(records):
    """Persist the contact list to the local JSON file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_contacts():
    """Load contacts from disk; seed sample data on first launch."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            # Corrupted file: fall back to seed data instead of crashing.
            pass
    seeded = [dict(record) for record in SEED_CONTACTS]
    save_contacts(seeded)
    return seeded


contacts = load_contacts()


def next_id():
    """Return the next unused contact id."""
    return max((record["id"] for record in contacts), default=0) + 1


# --------------------------------------------------------------------------- #
# Validation / normalization helpers
# --------------------------------------------------------------------------- #
def clean_list(value):
    """Turn a list or a delimited string into a cleaned list of non-empty strings."""
    if value is None:
        return []
    if isinstance(value, list):
        items = value
    else:
        items = re.split(r"[;,]", str(value))
    return [str(item).strip() for item in items if str(item).strip()]


def parse_bookmarked(value):
    """Interpret a Yes/No/True/1/star cell as a boolean."""
    return str(value or "").strip().lower() in BOOKMARK_TRUE_VALUES


def normalize_contact_payload(data, existing=None):
    """Validate and normalize an incoming contact payload."""
    if not isinstance(data, dict):
        raise ValueError("JSON body must be a contact object")

    name = str(data.get("name", "")).strip()
    if not name:
        raise ValueError("'name' is required")

    contact = existing or {}
    contact["name"] = name
    contact["bookmarked"] = bool(
        data.get("bookmarked", contact.get("bookmarked", False))
    )
    contact["phones"] = clean_list(data.get("phones", contact.get("phones", [])))
    contact["emails"] = clean_list(data.get("emails", contact.get("emails", [])))
    contact["socials"] = clean_list(data.get("socials", contact.get("socials", [])))
    contact["address"] = str(data.get("address", contact.get("address", ""))).strip()
    contact["note"] = str(data.get("note", contact.get("note", ""))).strip()
    return contact


# --------------------------------------------------------------------------- #
# Web page
# --------------------------------------------------------------------------- #
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "contacts": len(contacts)})


# --------------------------------------------------------------------------- #
# Contact CRUD API
# --------------------------------------------------------------------------- #
@app.route("/api/contacts", methods=["GET"])
def list_contacts():
    result = contacts

    if request.args.get("favorite") == "1":
        result = [record for record in result if record["bookmarked"]]

    query = request.args.get("q", "").strip().lower()
    if query:
        def matches(record):
            fields = (
                [record["name"], record["address"], record["note"]]
                + record["phones"]
                + record["emails"]
                + record["socials"]
            )
            return any(query in str(field).lower() for field in fields)

        result = [record for record in result if matches(record)]

    return jsonify(result)


@app.route("/api/contacts", methods=["POST"])
def create_contact():
    try:
        contact = normalize_contact_payload(request.get_json(silent=True) or {})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    contact["id"] = next_id()
    contacts.append(contact)
    save_contacts(contacts)
    return jsonify(contact), 201


@app.route("/api/contacts/<int:contact_id>", methods=["PUT"])
def update_contact(contact_id):
    contact = next((c for c in contacts if c["id"] == contact_id), None)
    if contact is None:
        return jsonify({"error": "Contact not found"}), 404

    try:
        contact = normalize_contact_payload(
            request.get_json(silent=True) or {}, existing=contact
        )
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    save_contacts(contacts)
    return jsonify(contact)


@app.route("/api/contacts/<int:contact_id>/bookmark", methods=["POST"])
def toggle_bookmark(contact_id):
    contact = next((c for c in contacts if c["id"] == contact_id), None)
    if contact is None:
        return jsonify({"error": "Contact not found"}), 404

    contact["bookmarked"] = not contact["bookmarked"]
    save_contacts(contacts)
    return jsonify(contact)


@app.route("/api/contacts/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    global contacts
    contact = next((c for c in contacts if c["id"] == contact_id), None)
    if contact is None:
        return jsonify({"error": "Contact not found"}), 404

    contacts = [c for c in contacts if c["id"] != contact_id]
    save_contacts(contacts)
    return jsonify({"deleted": contact_id})


# --------------------------------------------------------------------------- #
# Excel export / import
# --------------------------------------------------------------------------- #
def _build_workbook(records):
    """Build an .xlsx workbook: one header row, one row per contact."""
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Contacts"
    sheet.append(EXCEL_HEADERS)

    for record in records:
        sheet.append(
            [
                record["name"],
                "Yes" if record["bookmarked"] else "No",
                "; ".join(record["phones"]),
                "; ".join(record["emails"]),
                "; ".join(record["socials"]),
                record["address"],
                record["note"],
            ]
        )

    column_widths = [18, 12, 24, 28, 26, 32, 20]
    for index, width in enumerate(column_widths, start=1):
        sheet.column_dimensions[get_column_letter(index)].width = width
    return workbook


@app.route("/api/export-contacts.xlsx")
def export_excel():
    workbook = _build_workbook(contacts)
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name="contacts.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@app.route("/api/template.xlsx")
def template_excel():
    """Download a blank import template with one example row."""
    example = {
        "name": "Jane Doe",
        "bookmarked": False,
        "phones": ["139-0000-0000"],
        "emails": ["jane@example.com"],
        "socials": ["WeChat: jane_wx"],
        "address": "No. 2 Road, Fuzhou",
        "note": "Example row - edit or delete before import",
    }
    workbook = _build_workbook([example])
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name="address-book-template.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@app.route("/api/import", methods=["POST"])
def import_excel():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    uploaded = request.files["file"]
    if not uploaded.filename:
        return jsonify({"error": "Empty filename"}), 400

    try:
        workbook = load_workbook(uploaded, data_only=True)
    except Exception:
        return jsonify(
            {"error": "Cannot read the Excel file. Please upload a .xlsx file."}
        ), 400

    sheet = workbook.active
    rows = list(sheet.iter_rows(values_only=True))
    if not rows:
        return jsonify({"imported": 0, "skipped": 0, "message": "The file is empty."})

    # Resolve each canonical field to a column index through header aliases.
    header = [str(cell).strip().lower() if cell is not None else "" for cell in rows[0]]
    header_index = {name: idx for idx, name in enumerate(header)}

    def column_for(field):
        for alias in HEADER_ALIASES[field]:
            if alias in header_index:
                return header_index[alias]
        return None

    def cell_value(row, field):
        idx = column_for(field)
        if idx is None or idx >= len(row):
            return None
        return row[idx]

    imported = 0
    skipped = 0

    for raw_row in rows[1:]:
        if raw_row is None or all(
            value is None or str(value).strip() == "" for value in raw_row
        ):
            continue

        name = cell_value(raw_row, "name")
        if name is None or str(name).strip() == "":
            skipped += 1
            continue

        contact = {
            "id": next_id(),
            "name": str(name).strip(),
            "bookmarked": parse_bookmarked(cell_value(raw_row, "bookmarked")),
            "phones": clean_list(cell_value(raw_row, "phones")),
            "emails": clean_list(cell_value(raw_row, "emails")),
            "socials": clean_list(cell_value(raw_row, "socials")),
            "address": str(cell_value(raw_row, "address") or "").strip(),
            "note": str(cell_value(raw_row, "note") or "").strip(),
        }
        contacts.append(contact)
        imported += 1

    save_contacts(contacts)
    return jsonify({"imported": imported, "skipped": skipped})


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # host=0.0.0.0 makes the app reachable on the local network; for the
    # optional cloud deployment see docs/team-guide.md.
    app.run(host="0.0.0.0", port=5000, debug=False)
