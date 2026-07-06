"""
extract_staff_attachments.py
-----------------------------
Scans the salary "email attachment" files (Excel .xlsx / .xlsm and CSV) for a
given staff name and copies every file that contains that name into a single
output folder.

The staff name is matched INSIDE the file content (cell values / rows), since
the salary attachments are named by month/year and the staff names live inside.

Usage:
    python extract_staff_attachments.py
"""

import csv
import os
import re
import shutil

import openpyxl

# --- Configuration ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Folders that hold the original salary email attachments.
SOURCE_FOLDERS = [
    os.path.join(BASE_DIR, "legacy_payroll_files"),
    os.path.join(BASE_DIR, "Cleaned Data"),
]

# The staff name we are looking for (case-insensitive, spacing-tolerant).
TARGET_NAME = "MAIMUNA IZAH"

# Where matching attachments are copied to.
OUTPUT_FOLDER = os.path.join(BASE_DIR, "MAIMUNA_IZAH_Salary_Attachments")

# File types we treat as salary attachments.
EXCEL_EXTS = (".xlsx", ".xlsm")
CSV_EXTS = (".csv",)


def build_name_pattern(name):
    """Build a regex that matches the name even if spacing differs.

    e.g. "MAIMUNA IZAH" -> matches "MAIMUNA  IZAH", "MAIMUNA\tIZAH", etc.
    Also tolerant of the parts appearing in the order given.
    """
    parts = [re.escape(p) for p in name.split()]
    return re.compile(r"\s+".join(parts), re.IGNORECASE)


NAME_PATTERN = build_name_pattern(TARGET_NAME)


def normalize(text):
    """Collapse all whitespace so multi-cell / multi-space names still match."""
    return re.sub(r"\s+", " ", str(text)).strip()


def excel_contains_name(file_path):
    """Return True if any cell in any sheet contains the target name."""
    try:
        wb = openpyxl.load_workbook(file_path, data_only=True, read_only=True)
    except Exception as exc:
        print(f"   [WARN] Could not open Excel '{os.path.basename(file_path)}': {exc}")
        return False

    found = False
    try:
        for sheet in wb.worksheets:
            for row in sheet.iter_rows(values_only=True):
                # Join the whole row so a name split across adjacent cells
                # (first name | last name) is still detected.
                row_text = normalize(" ".join("" if c is None else str(c) for c in row))
                if NAME_PATTERN.search(row_text):
                    found = True
                    break
            if found:
                break
    finally:
        wb.close()
    return found


def csv_contains_name(file_path):
    """Return True if any row in the CSV contains the target name."""
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            with open(file_path, newline="", encoding=encoding) as fh:
                reader = csv.reader(fh)
                for row in reader:
                    row_text = normalize(" ".join(row))
                    if NAME_PATTERN.search(row_text):
                        return True
            return False
        except UnicodeDecodeError:
            continue
        except Exception as exc:
            print(f"   [WARN] Could not read CSV '{os.path.basename(file_path)}': {exc}")
            return False
    return False


def file_contains_name(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in EXCEL_EXTS:
        return excel_contains_name(file_path)
    if ext in CSV_EXTS:
        return csv_contains_name(file_path)
    return False


def unique_destination(folder, filename):
    """Avoid overwriting files that share a name across source folders."""
    dest = os.path.join(folder, filename)
    if not os.path.exists(dest):
        return dest
    stem, ext = os.path.splitext(filename)
    i = 2
    while os.path.exists(os.path.join(folder, f"{stem} ({i}){ext}")):
        i += 1
    return os.path.join(folder, f"{stem} ({i}){ext}")


def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    print(f"Searching for '{TARGET_NAME}' inside salary attachments...\n")

    matched = []
    scanned = 0

    for folder in SOURCE_FOLDERS:
        if not os.path.isdir(folder):
            print(f"[SKIP] Source folder not found: {folder}")
            continue

        print(f"Scanning folder: {folder}")
        for filename in sorted(os.listdir(folder)):
            file_path = os.path.join(folder, filename)
            if not os.path.isfile(file_path):
                continue
            if os.path.splitext(filename)[1].lower() not in (EXCEL_EXTS + CSV_EXTS):
                continue

            scanned += 1
            if file_contains_name(file_path):
                dest = unique_destination(OUTPUT_FOLDER, filename)
                shutil.copy2(file_path, dest)
                matched.append(filename)
                print(f"   [MATCH] {filename}  ->  copied")
        print()

    print("=" * 60)
    print("DONE")
    print(f"Files scanned : {scanned}")
    print(f"Files matched : {len(matched)}")
    print(f"Output folder : {OUTPUT_FOLDER}")
    print("=" * 60)
    if matched:
        print("\nMatched attachments:")
        for name in matched:
            print(f"  - {name}")


if __name__ == "__main__":
    main()
