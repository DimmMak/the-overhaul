#!/usr/bin/env python3
"""
validate-skill.py — SKILL.md frontmatter validator

Reads a SKILL.md file, parses YAML frontmatter, validates against the schema
at future-proof/data/skill-md-schema.json. Returns exit 0 on pass, 1 on fail
with detailed error messages.

Used by install.sh in every skill to gate installation.

Usage:
  python3 validate-skill.py /path/to/SKILL.md
  python3 validate-skill.py --schema-version 0.1 /path/to/SKILL.md   # override schema level

Exit codes:
  0 = pass
  1 = validation failed (schema violation)
  2 = file not found or unreadable
  3 = schema not found
"""
import json
import sys
import re
from pathlib import Path


SCHEMA_PATH = Path(__file__).resolve().parent.parent / "data" / "skill-md-schema.json"

# Schema enforcement level. v0.1 = S1 fields only. v0.2 = S2 fields (capabilities required).
# Controlled via --schema-version CLI flag or env var SKILL_SCHEMA_VERSION.
DEFAULT_SCHEMA_VERSION = "0.3"  # S3 enforcement: unix_contract block required


def load_schema():
    if not SCHEMA_PATH.exists():
        print(f"❌ schema not found at {SCHEMA_PATH}", file=sys.stderr)
        sys.exit(3)
    return json.loads(SCHEMA_PATH.read_text())


def parse_frontmatter(skill_md_path):
    """Extract YAML frontmatter from a SKILL.md — returns dict of fields."""
    text = skill_md_path.read_text()
    # Frontmatter is between first pair of `---` markers
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return None
    fm_text = match.group(1)

    # Parse simple key-value lines (no full YAML; keeps deps minimal)
    fields = {}
    current_key = None
    current_value_lines = []
    for line in fm_text.splitlines():
        if not line.strip():
            continue
        # Top-level key
        m = re.match(r"^([a-zA-Z_][\w-]*):\s*(.*)$", line)
        if m and not line.startswith(" ") and not line.startswith("\t"):
            # Finalize previous key
            if current_key is not None:
                fields[current_key] = "\n".join(current_value_lines).strip() if current_value_lines else fields.get(current_key, "")
            key = m.group(1)
            value = m.group(2).strip()
            if value in (">", "|"):
                # Multi-line value follows
                current_key = key
                current_value_lines = []
                fields[key] = ""
            else:
                fields[key] = value
                current_key = None
                current_value_lines = []
        else:
            # Continuation line
            if current_key is not None:
                current_value_lines.append(line.strip())

    # Finalize last key
    if current_key is not None and current_value_lines:
        fields[current_key] = "\n".join(current_value_lines).strip()

    # Stash full raw frontmatter text for nested-block checks (e.g., capabilities:)
    fields["_raw_text"] = fm_text

    return fields


def validate(fields, schema, level):
    """Run schema checks. Returns (ok: bool, errors: list[str])."""
    errors = []

    # Required fields per level
    required = ["name", "domain", "description"]

    for req in required:
        if req not in fields or not fields[req]:
            errors.append(f"missing required field: `{req}`")

    # v0.2+: capabilities block required.
    if level in ("0.2", "0.3"):
        if "_raw_text" in fields:
            raw = fields["_raw_text"]
            if "capabilities:" not in raw:
                errors.append("missing required `capabilities:` block (v0.2+ requires reads/writes/calls/cannot)")
            else:
                for subkey in ("reads:", "writes:", "calls:", "cannot:"):
                    if subkey not in raw:
                        errors.append(f"capabilities block missing `{subkey}` sub-field")

    # v0.3+: unix_contract block required.
    if level == "0.3":
        if "_raw_text" in fields:
            raw = fields["_raw_text"]
            if "unix_contract:" not in raw:
                errors.append("missing required `unix_contract:` block (v0.3 requires data_format/schema_version/stdin_support/stdout_format/composable_with)")
            else:
                for subkey in ("data_format:", "schema_version:", "stdin_support:", "stdout_format:", "composable_with:"):
                    if subkey not in raw:
                        errors.append(f"unix_contract block missing `{subkey}` sub-field")

    # name — kebab-case
    name = fields.get("name", "")
    if name and not re.match(r"^[a-z][a-z0-9-]*$", name):
        errors.append(f"invalid name `{name}` — must be kebab-case (lowercase, hyphens only)")

    # domain — enum
    domain = fields.get("domain", "")
    valid_domains = ["fund", "learning", "general"]
    if domain and domain not in valid_domains:
        errors.append(f"invalid domain `{domain}` — must be one of: {', '.join(valid_domains)}")

    # version — semver
    version = fields.get("version", "")
    if version and not re.match(r"^\d+\.\d+\.\d+$", version):
        errors.append(f"invalid version `{version}` — must be semver (e.g., 0.1.0)")

    # description — length
    desc = fields.get("description", "")
    if desc:
        # Strip continuation whitespace for length check
        desc_clean = re.sub(r"\s+", " ", desc).strip()
        if len(desc_clean) < 50:
            errors.append(f"description too short ({len(desc_clean)} chars) — minimum 50, explain what the skill does + triggers")
        if len(desc_clean) > 2000:
            errors.append(f"description too long ({len(desc_clean)} chars) — maximum 2000, move detail into body")

    # NOT-for clause enforcement (collision fence) — required if 2+ skills exist
    if desc and "NOT for:" not in desc:
        errors.append("missing `NOT for:` collision-fence clauses in description (list 2+ sibling skills to avoid)")

    return (len(errors) == 0, errors)


def main():
    args = sys.argv[1:]
    level = DEFAULT_SCHEMA_VERSION
    paths = []
    i = 0
    while i < len(args):
        if args[i] == "--schema-version" and i + 1 < len(args):
            level = args[i + 1]
            i += 2
        else:
            paths.append(args[i])
            i += 1

    if not paths:
        print("usage: validate-skill.py [--schema-version 0.1|0.2] /path/to/SKILL.md", file=sys.stderr)
        sys.exit(2)

    schema = load_schema()
    any_failed = False

    for path_str in paths:
        path = Path(path_str)
        if not path.exists():
            print(f"❌ {path}: file not found", file=sys.stderr)
            any_failed = True
            continue

        fields = parse_frontmatter(path)
        if fields is None:
            print(f"❌ {path}: no frontmatter found (missing `---` markers)", file=sys.stderr)
            any_failed = True
            continue

        ok, errors = validate(fields, schema, level)
        if ok:
            print(f"✅ {path}: passes schema v{level}")
        else:
            print(f"❌ {path}: {len(errors)} violation(s)", file=sys.stderr)
            for err in errors:
                print(f"   - {err}", file=sys.stderr)
            any_failed = True

    sys.exit(1 if any_failed else 0)


if __name__ == "__main__":
    main()
