# AGENTS.md

Guidance for AI agents working in this repo.

## Project

Thea — worldbuilding for a hard-SF fiction project. See `CONTEXT.md`.

## Rules

- Keep the science accurate. Flag speculation as speculation.
- Match the established prose style: spare, plain, short declarative sentences.
- Don't pad. Don't editorialize.

## Files

- `CONTEXT.md` — world, canon, and research state
- `timeline.csv` — full solar system timeline
- `characters/` — one file per character
- `<unix-timestamp>/` — one folder per anchor moment, named for its
  Unix timestamp in seconds. Each holds `context.md` and a
  fine-resolution `timeline.csv`. See CONTEXT.md for the convention.
- `earth/` — continental maps across time. `earth.csv` holds climate
  keyframes; `build.py` renders 0.25° frames (0-1800 Ma). Frames live
  in the `earth-frames` GitHub release, not in git.

<!-- Add conventions here as they emerge. -->
