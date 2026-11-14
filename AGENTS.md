# AGENTS.md

Guidance for AI agents working in this repo.

## Project

Thea — worldbuilding for a hard-SF fiction project. See `CONTEXT.md`.

## Rules

- Keep the science accurate. Flag speculation as speculation.
- Match the established prose style: spare, plain, short declarative sentences.
- Don't pad. Don't editorialize.
- Before giving any number for a time-point folder, read its `assumptions.md` and use the value registered there. If a value is missing, add an ID with its status. Don't invent one silently.
- Status words in `assumptions.md`:
  - `canon`: fixed for all stories.
  - `provisional`: a value chosen with low or medium confidence. Usable; flag it.
  - `open`: needs checking before any story relies on it.
  - `speculative`: an idea with no value yet. Not used in canon.
- Cite assumption IDs (e.g. A-003) instead of restating values. When a value changes, update every file in its "Depends on" column.

## Files

- `CONTEXT.md` — world, canon, and research state
- `timeline.csv` — full solar system timeline
- `characters/` — one file per character
- `<unix-timestamp>/` — one folder per anchor moment, named for its
  Unix timestamp in seconds. Each holds `context.md`, a
  fine-resolution `timeline.csv`, and `assumptions.md` (the chosen
  values and their status). See CONTEXT.md for the convention.
- `earth/` — Earth maps across time. `build.py` makes `earth.nc`
  (0.25°, 0-1800 Ma plus whole-planet state frames and Pangaea Proxima
  at +250 Myr; `frames.csv` maps state frames to time windows). Inputs and
  citations in `earth/sources/`; downloads and output in `earth/work/`
  (gitignored). GitHub Actions (`.github/workflows/earth.yml`) rebuilds
  and publishes the `earth-frames` release when build.py or sources change.

<!-- Add conventions here as they emerge. -->
