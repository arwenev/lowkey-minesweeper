# Lowkey Minesweeper

I got bored at work so I created a Minesweeper disguised as a "Console Debugger" window, built so it looks like legitimate dev output at a glance.

## Setup

**Easiest way:** run the setup script for your OS. It creates a virtual environment, installs dependencies, and launches the game.

- macOS/Linux: `./setup.sh`
- Windows: double-click `setup.bat` (or run it from a terminal)

**Manual way:**

```
pip install -r requirements.txt
python3 minesweeper.py
```

## Controls

| Action | Result |
|---|---|
| Left click | Reveal a cell |
| Right click | Flag / unflag a cell |
| Double click | Chord — reveal neighbors once the flag count around a number matches it |
| `Esc` | Toggle the panic screen |

## The panic screen

This is the actual point of the disguise — a boss key.

The window is titled "Console Debugger" and normally shows a fake log line (`// STACK_TRACE_LOG: MINES_LEFT: ...`) above the grid, so even mid-game it reads as debugging output rather than a game. Pressing `Esc` goes a step further: it instantly swaps the entire game view for a block of fake JSON that looks like real process output (`"status": "success"`, `"records_processed": 4810`, etc.), while the title bar still reads "Console Debugger."

If someone glances at your screen while you're playing, one tap of `Esc` makes it look like you're staring at legitimate work output. Press `Esc` again and it flips straight back to the game, exactly where you left off — nothing resets.

### Making your own

The panic screen content lives in its own file, `panic_screen.py` — no need to touch the game logic to change it.

Open `panic_screen.py` and either:
- pick one of the built-in presets (`console_log`, `build_output`, `spreadsheet`) by changing `ACTIVE_PRESET`, or
- write your own fake output under `PRESETS["custom"]` and set `ACTIVE_PRESET = "custom"`

You can also change `PANIC_TEXT_COLOR` there to match whatever look you're going for.

## Files

- `minesweeper.py` — the native PySide6 desktop app (recommended; no browser restrictions)
- `panic_screen.py` — panic screen content, edit this to customize your own disguise
- `requirements.txt` — dependencies (just PySide6)
- `setup.sh` / `setup.bat` — one-step setup + launch for macOS/Linux and Windows
- `index.html` — original browser-based version
