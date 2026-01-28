#!/usr/bin/env python3
"""
generate_roster.py — dependency-free HTML roster generator

Usage:
  python generate_roster.py config.json output.html

Notes:
- Designed for printing to Letter landscape.
- Produces a single static HTML file (no JS required).
- You can type names/notes in-browser (contenteditable) before printing.
"""

import json
import sys
from pathlib import Path
from html import escape


def load_config(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"Config JSON parse error: {e}")


def require(config: dict, key: str, typ):
    if key not in config:
        raise SystemExit(f"Missing required config key: {key}")
    if not isinstance(config[key], typ):
        raise SystemExit(f"Config key '{key}' must be {typ.__name__}")
    return config[key]


def opt(config: dict, key: str, default):
    return config.get(key, default)


def build_th_milestones(columns):
    return "\n      ".join([f'<th class="col-m">{escape(col)}</th>' for col in columns])


def build_tbody_rows(roster_size, columns):
    cols_n = len(columns)
    rows = []
    for i in range(1, roster_size + 1):
        checks = "\n      ".join(['<td class="col-m"><span class="checkbox"></span></td>' for _ in range(cols_n)])
        row = (
            '<tr>\n'
            f'      <td class="col-num">{i}</td>\n'
            '      <td class="col-name">\n'
            '        <span class="editable" contenteditable="true" data-placeholder="(type name)"></span>\n'
            '        <span class="notes-line"></span>\n'
            '      </td>\n'
            f'      {checks}\n'
            '      <td class="col-notes">\n'
            '        <span class="editable" contenteditable="true" data-placeholder="(notes)"></span>\n'
            '        <span class="notes-line"></span>\n'
            '      </td>\n'
            '    </tr>'
        )
        rows.append(row)
    return "\n    ".join(rows)


def build_legend_items(legend_pairs):
    parts = []
    for item in legend_pairs:
        if isinstance(item, dict):
            label = item.get("label", "")
            text = item.get("text", "")
        elif isinstance(item, (list, tuple)):
            label = item[0] if len(item) > 0 else ""
            text = item[1] if len(item) > 1 else ""
        else:
            label, text = "", ""
        parts.append(f'<div><strong>{escape(label)}:</strong> {escape(text)}</div>')
    return "\n    ".join(parts)


def render(template: str, mapping: dict) -> str:
    out = template
    for k, v in mapping.items():
        out = out.replace("{{" + k + "}}", v)
    return out


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python generate_roster.py config.json output.html")

    config_path = Path(sys.argv[1]).expanduser().resolve()
    out_path = Path(sys.argv[2]).expanduser().resolve()
    template_path = Path(__file__).parent / "roster.template.html"

    if not config_path.exists():
        raise SystemExit(f"Config not found: {config_path}")
    if not template_path.exists():
        raise SystemExit(f"Template not found next to script: {template_path}")

    config = load_config(config_path)

    course_title = require(config, "course_title", str)
    subtitle = opt(config, "subtitle", "Roster")
    roster_size = require(config, "roster_size", int)
    columns = require(config, "columns", list)

    if roster_size < 1 or roster_size > 40:
        raise SystemExit("roster_size must be between 1 and 40 for this layout.")
    if not all(isinstance(c, str) and c.strip() for c in columns):
        raise SystemExit("columns must be a non-empty list of strings.")

    doc_title = opt(config, "doc_title", f"Roster — {course_title}")
    legend_title = opt(config, "legend_title", "Legend")
    feedback_script = opt(
        config,
        "feedback_script",
        "Glow (what’s working) + Grow (one next step) + Choice (story / challenge / polish)",
    )

    legend_items = opt(config, "legend_items", None)
    if legend_items is None:
        legend_items = [{"label": c, "text": ""} for c in columns]

    template = template_path.read_text(encoding="utf-8")

    mapping = {
        "DOC_TITLE": escape(doc_title),
        "H1_TITLE": escape(f"{course_title} — {subtitle}"),
        "TH_MILESTONES": build_th_milestones(columns),
        "TBODY_ROWS": build_tbody_rows(roster_size, columns),
        "LEGEND_TITLE": escape(legend_title),
        "LEGEND_ITEMS": build_legend_items(legend_items),
        "FEEDBACK_SCRIPT": escape(feedback_script),
    }

    html = render(template, mapping)
    out_path.write_text(html, encoding="utf-8")
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
