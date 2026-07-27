"""
Panic Screen Config
--------------------
This is what shows up when you hit Esc mid-game. Edit it to make your
own disguise — nothing in minesweeper.py needs to change.

Quick start: change ACTIVE_PRESET below to pick a built-in look, or
write your own text under PRESETS["custom"] and set
ACTIVE_PRESET = "custom".
"""

PRESETS = {
    "console_log": """{
  "status": "success",
  "timestamp": "2026-07-27T10:19:00Z",
  "data": {
    "sync_completed": true,
    "records_processed": 4810,
    "execution_time_ms": 112,
    "buffer_allocation": "0x7fff5fbff610",
    "active_workers": [
      {"id": "worker-0", "load": "4.2%"},
      {"id": "worker-1", "load": "2.1%"}
    ]
  }
}""",

    "build_output": """> npm run build

> project@1.0.0 build
> webpack --mode production

asset main.[hash].js 842 KiB [emitted] [minimized]
asset index.html 1.2 KiB [emitted]
runtime modules 1.06 KiB 5 modules
modules by path ./src/ 412 KiB 87 modules
webpack compiled successfully in 4821 ms

watching for file changes...""",

    "spreadsheet": """Recalculating workbook...
Sheet1!A1:D240 - formulas evaluated: 960
Sheet1!E:E - VLOOKUP chain resolved (3 levels)
PivotTable_1 refreshed - 14,203 rows
Autosave: complete (11:42:03)
No errors found.""",

    # Write your own fake output here, then set ACTIVE_PRESET = "custom" below.
    "custom": """Write your own fake output here.""",
}

# Falls back to this preset if ACTIVE_PRESET below is ever misspelled,
# left blank, or points at a preset you later delete. Always keep this
# pointing at something that exists in PRESETS.
DEFAULT_PRESET = "console_log"

# Which preset to actually display. One of: "console_log", "build_output",
# "spreadsheet", "custom" — or the name of any new key you add to PRESETS above.
ACTIVE_PRESET = "console_log"

# Text color for the panic screen (hex string).
PANIC_TEXT_COLOR = "#9cdcfe"

if ACTIVE_PRESET not in PRESETS:
    print(
        f"[panic_screen] Unknown ACTIVE_PRESET '{ACTIVE_PRESET}', "
        f"falling back to '{DEFAULT_PRESET}'."
    )
    ACTIVE_PRESET = DEFAULT_PRESET

PANIC_TEXT = PRESETS[ACTIVE_PRESET]
