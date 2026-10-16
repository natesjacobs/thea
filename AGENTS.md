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
- `earth/` — Earth maps across time. `build.py` makes `earth.nc`
  (0.25°, 0-1800 Ma: land, elevation, temperature, class). Inputs and
  citations in `earth/sources/`; downloads and output in `earth/work/`
  (gitignored). GitHub Actions (`.github/workflows/earth.yml`) rebuilds
  and publishes the `earth-frames` release when build.py or sources change.

<!-- Add conventions here as they emerge. -->
