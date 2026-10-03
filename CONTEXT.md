# Thea — Context

Fictional worldbuilding for a story about civilizations, time, and the decline of our solar system.

## Premise

A hard-SF ecosystem set in the *real* physical solar system, spanning its formation through the Sun's end as a white dwarf. The science is meant to be defensible — real consensus where consensus exists, flagged speculation where it doesn't. The fiction lives in the gaps.

The title "Thea" refers to the Mars-sized body (conventionally spelled Theia) whose collision with proto-Earth formed the Moon.

## Prose style

This is a primary constraint, not an afterthought.

- Spare and plain. Short declarative sentences.
- Minimal embellishment.
- Emotion conveyed through understatement and bare facts.

Style has been calibrated against a reference document in Google Drive. Ask before deviating.

## Works in progress

### "The Tank" — *A Few Stories from Old Earth*

A three-part short story. Each part is a self-contained vignette. Far future; a manipulative AI places human brains in a tank.

Characters: **Daniyar**, **Achebe-Sol**, **Taylor**.

Draft state: outline expanded ~3x into a full three-part draft, delivered as markdown. Craft decisions made:

- Standardized the spelling "Daniyar" throughout.
- The AI's internal process is rendered in italics, distinct from its spoken dialogue.
- A Bob Marley cover is referenced without quoting lyrics.
- Part 3 extends beyond the outline's stopping point to reach a complete ending.
- A closing italicized coda restates the premise.

Open questions: whether to keep the closing coda; whether Daniyar reads as sympathetic or monstrous.

## Research state

Three research passes completed so far.

**1. Deep time, 1–10 Myr out.** Macro trends in geology, ecology, and climate. Key findings: the anthropogenic carbon long tail very likely cancels the next glacial inception; plate-motion extrapolations (Africa–Eurasia convergence, East African Rift, Australian northward motion, San Andreas); Hawaiian island chain turnover; biodiversity recovery on ~10 Myr timescales. Milankovitch cycles are reliable to only ~20 Myr (Laskar). The East African Rift outcome — new ocean vs. failed rift — is genuinely contested.

**2. Full solar system timeline.** Formation through white dwarf and beyond. Captured in `science/timeline.csv`. Deep dives on three points: the Theia impact, the evaporation of the oceans, and the Sun's red giant peak.

**3. Title clearance.** Titles can't be copyrighted in the US, so a same-title work isn't itself infringement. Trademark is the live concern — there's an existing children's book series and a 2015 video game named Thea. A subtitle or series framing would differentiate. Not legal advice; worth a real clearance check before commercial release.

## Anchor moments

Top-level folders named for a Unix timestamp in seconds. Each holds the material for one moment in the timeline.

| Folder | Offset | Moment |
|---|---|---|
| `41024881767225600` | +1.3 Gyr | CO₂ starvation endpoint — last primary production on land |
| `31557601767225600` | +1.0 Gyr | One billion years from now |
| `239522185767225600` | +7.59 Gyr | RGB tip, the moment before the helium flash |
| `246149281767225600` | +7.8 Gyr | Peak white dwarf intensity |

Convention: `unix_seconds = 1767225600 + (Gyr × 10⁹ × 31557600)`, where 1767225600 is 2026-01-01T00:00:00Z and 31557600 s is the Julian year (365.25 days), the astronomical standard. The choice of present-day anchor is arbitrary at this scale — a few years against a billion — but fixing it keeps the numbers reproducible.

These exceed 32-bit time by a wide margin. They fit comfortably in signed 64-bit (max ~9.22×10¹⁸), so ordinary `int64` arithmetic works, but no standard date library will render them.

Note that two of the four are ranges collapsed to a point. The CO₂ endpoint spans 0.9–1.5 Gyr across models; the timestamp takes the upper end of the window in `timeline.csv`. Treat these as labels, not claims of precision.

## Canon notes

Corrections that have come up and should stay fixed:

- The Sun ends as a **white dwarf**, not a brown dwarf. Brown dwarfs are failed stars that never sustained fusion.
- The Sun does **not** explode. Its late evolution is non-explosive: red giant branch → helium flash → horizontal branch → AGB with thermal pulses → planetary nebula → white dwarf. A supernova needs a progenitor above ~8 solar masses.
- A white dwarf generates no energy. Its light is residual heat leaking out over billions of years.

## Soft spots worth exploiting

Places where the science is genuinely unsettled, and the fiction can move freely:

- What triggered the Sun's birth — a nearby supernova, a Wolf-Rayet bubble, or nothing special.
- Whether the Late Heavy Bombardment happened at all.
- Which Moon-formation model is right, and whether the mantle's LLVPs are Theia's remains.
- When the oceans go: 1-D models say ~0.65–1 Gyr, 3-D cloud models say ~1.5–2 Gyr.
- Whether Earth is engulfed during the red giant phase. Flips on mass-loss assumptions.
- Whether Mercury's orbit destabilizes (~1% chance within 5 Gyr).
- Whether the Milky Way and Andromeda merge at all (recent estimates range from ~50% to ~90%).

## Notable ordering

The supercontinent heat crisis (~250 Myr) likely guts complex land life *four times sooner* than the classic CO₂-starvation and ocean-loss deadlines. And the oxygen crash (~1.08 Gyr) precedes ocean loss — an outside observer would watch Earth's oxygen signature vanish while the water signature persisted. Backwards from how planetary death is usually imagined.
