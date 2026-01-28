# Roster Generator Kit (HTML)

A tiny, dependency‑free tool that turns a `config.json` into a **printable Letter‑landscape HTML roster sheet**.

This is built for **fast, feedback‑based classroom tracking**: checkboxes for milestones + a notes lane.

---

## What’s in this kit

- `generate_roster.py` — generator script (Python 3, no dependencies)
- `roster.template.html` — the print layout with placeholders
- `config_examples/`
  - `scratch_big_six.json` — 6 milestone version (Save/Controls/L1/Cutscene/L2/Full Run)
  - `scratch_weekly_12.json` — 12 week checkboxes (W1–W12)
  - `blank_config.json` — copy/paste starter for any course

---

## Quick start

From inside the kit folder:

```bash
python generate_roster.py config_examples/scratch_big_six.json roster.html
```

Open `roster.html` in a browser → **Print** → “Save as PDF” (or print paper).

---

## Generation notes

### 1) Printing settings (important)
For best results in Chrome/Edge/Firefox:
- Paper: **Letter**
- Orientation: **Landscape**
- Margins: **Default** (the file uses page margins already)
- Scale: **100%** (if columns clip, try 95–98%)
- Headers/footers: **Off**
- Background graphics: **Off** (fine either way)

### 2) Editing names/notes before printing
The generated roster uses `contenteditable`, so you can:
- click the **Student Name** cell and type names
- click the **Notes** cell and type quick notes

Then print to PDF and you’ll have a “filled in” copy.

### 3) Recommended folder workflow (template library)
Keep the kit stable, and version your course configs:

```
roster-tool/            # this kit (rarely changes)
configs/                # your evolving course snapshots
  2026_Spring_Scratch_BigSix.json
  2026_Spring_Scratch_Weekly.json
  2026_Summer_Robotics_Checkpoints.json
outputs/                # generated artifacts (disposable)
  Scratch_BigSix_roster.html
  Scratch_BigSix_roster.pdf
```

A simple habit that scales:
- Edit only **config files**
- Re‑generate rosters whenever you need a clean sheet

### 4) Naming convention (suggested)
- Configs: `YYYY_Term_Course_SheetType.json`
- Outputs: `Course_SheetType_roster.html` and `.pdf`

---

## Config reference

### Required keys
- `course_title` (string)
- `roster_size` (int)
- `columns` (list of strings)

### Optional keys
- `subtitle` (string)
- `doc_title` (string)
- `legend_title` (string)
- `legend_items` (list of objects like `{"label": "...", "text": "..."}`)
- `feedback_script` (string)

### Example: Big Six (milestones)
```json
{
  "course_title": "Scratch Game Studio",
  "subtitle": "Big Six Milestones Roster",
  "roster_size": 18,
  "columns": ["Save","Controls","L1 Goal","Cutscene","Level 2","Full Run"]
}
```

---

## Fit and layout guidance

This layout is tuned for:
- **~6–12 columns** (checkbox columns)
- **up to ~40 students**

If you exceed that:
- Prefer fewer columns (e.g., Big Six instead of 12‑week detail), or
- Make a second roster sheet type (two configs, two outputs)

If columns clip at the right edge:
- In print dialog, set **Scale to 95–98%**, or
- Shorten column headings (e.g., “Controls” instead of “Player Controls”)

---

## Troubleshooting

### “python is not recognized”
- On some systems use: `python3` instead of `python`

### “Permission denied” running the script
- Use: `python generate_roster.py ...` (always works)

### I double‑clicked the HTML and it looks weird
- It should still print correctly.
- If it looks zoomed, reset browser zoom to 100% before printing.

### I want checkmarks instead of empty boxes
This is intentionally paper‑first. If you want “click to toggle” checkboxes digitally,
we can add an optional JS mode that toggles boxes and prints the state.

---

## Common extensions (easy upgrades)

If you want to evolve this into a “course printing press,” typical next additions are:
- **multi‑sheet generation** from one config (Big Six + Weekly + conference notes)
- **CSV import** (student names auto‑filled from a roster file)
- **auto PDF export** (headless Chrome command; useful for batch output)
- **different page sizes** (A4, legal, etc.)

Tell me your preferred “next” and I’ll shape the tool to match your workflow.

---

_Last updated: 2026-01-28_
