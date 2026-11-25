# Last year's approach 1

One modeled approach, worked out in detail. Not canon: the anchor's `context.md` and `timeline.csv` keep options open. Stories may lock it in.

Assumptions: contact per A-002, A-003, A-009 and A-010 in `assumptions.md`; orbits per A-011 to A-013. Theia on a neighbouring orbit slightly outside Earth's. One approach direction, chosen as the lowest-eccentricity lane with Theia outside. Another direction changes where each body sits in the other's sky and the impact's local time. Reproduce with `python3 -I approach_run.py`; `scan` shows the other directions.

## The run

- Three bodies: the Sun, proto-Earth and Theia. Point masses, one plane.
- Started at contact and integrated backward one year. Contact at 9.5 km/s means ~2.6 km/s of approach speed far out.
- Orbits one year out:

| | Proto-Earth | Theia |
|---|---|---|
| Semi-major axis | 0.999 AU | 1.013 AU |
| Eccentricity | 0.011 | 0.077 |
| Year | 365 days | 372 days |

The two orbits share a lane but not a shape. At 2.6 km/s far out, Theia's eccentricity cannot drop below ~0.08 in any direction. Its orbit dips inside Earth's and swings back out.

Inputs come from the papers cited in `context.md`. Everything computed from them here, including every brightness, is modeled, not published. Brightness assumes reflectivity 0.15 for Theia (rock) and 0.3 for Earth (cloud).

## The closing distance

| Before impact | Distance | Relative speed | Theia's size from Earth |
|---|---|---|---|
| 1 yr | 19 million km (0.13 AU) | 1.1 km/s | 1.3′ |
| 6 mo | 43 million km (0.29 AU) | 5.8 km/s | 0.6′ |
| 3 mo | 29 million km | 5.6 km/s | 0.8′ |
| 1 mo | 7.6 million km | 3.3 km/s | 3.2′ |
| 2 wk | 3.4 million km | 2.8 km/s | 7.0′ |
| 1 wk | 1.8 million km | 2.7 km/s | 14′ |
| 5.6 d | 1.43 million km. Enters Earth's Hill sphere. From here it is falling | 2.7 km/s | 17′ |
| 3 d | 820,000 km | 2.8 km/s | 29′ |
| 30 hr | 384,000 km, today's Moon distance | — | ~1.1° |
| 1 d | 320,000 km | 3.1 km/s | 1.3° |
| 12 hr | 183,000 km | 3.4 km/s | 2.2° |
| 6 hr | 108,000 km | 3.8 km/s | 3.7° |
| 1 hr | 31,000 km | 5.7 km/s | 13° |
| 23 min | 18,500 km. Crosses the Roche limit | — | ~22° |
| 10 min | 13,700 km | 8.1 km/s | 29° |
| 0 | contact | 9.5 km/s | horizon to horizon |

The distance does not shrink steadily. Over the year Theia loops around Earth. Seen from Earth, with the Sun held below:
- **A year out:** 0.13 AU away, west of the Sun, closing slowly.
- **Ten months out:** directly opposite the Sun.
- **Six months out:** swung out to 0.29 AU, east of the Sun.
- **Last month:** falling in from the sunward side.

## Theia from Earth

**Why it came out of the evening twilight.** Theia's orbit was slightly larger but more stretched. A year out it was west of the Sun, a morning object. It passed opposition, then drifted east into the evening sky and sank toward the Sun for months. In the last weeks it was a thin crescent close to the Sun, approaching Earth from almost the Sun's direction.

| Before impact | Where | Size | Brightness | Lit |
|---|---|---|---|---|
| 12–11 mo | Pre-dawn, 89° then 114° west of the Sun | 1.3–1.4′ | mag −5 to −5.6, brighter than Venus | 56 → 75% |
| 10 mo | 157° west, rising in the evening | 1.8′ | mag −6.5 | 97% |
| 9.6 mo (292 d) | **Opposition.** Opposite the Sun. Up all night, highest at midnight | ~1.6′ | mag −6.5 | full |
| 9–7 mo | Evening sky, 149° then 101° east | 1.4 → 0.7′ | mag −6 to −4 | 94 → 70% |
| 6–3 mo | Evening, 89° then 63° east | 0.6–0.8′, a point | mag −3.3, like Venus | 63 → 35% |
| 2–1 mo | Evening, 50° then 31° east | 1.4 → 3.1′ | mag −3.7 | 22 → 8% |
| Last 3 wk | Low in the west after sunset, sinking into twilight, 23° then 11° east | 5–14′ | mag −3.5 | 4 → 1% |
| 2 d | **Closest to the Sun, 8° east.** Lost in the glare | ~40′ | — | 1% |
| Last day | 9° then 15° east. A daytime object | 1.3° to 3.7° | mag −6 to −10 | 1 → 2% |
| Last hour | Pulls away east of the Sun, 33° to 73° by contact | 13° to 38° | mag −16 to −21 | 8 → 35% |

- **It arrived as a crescent.** For the last month Earth was looking at Theia's night side.
- **The night side glowed.** It was lit by Earth, which from Theia was full and brighter than our full Moon. Today's faint earthshine on a crescent Moon gives the idea, made far stronger.
- **It hid in the Sun's glare.** For the last week it sat within ~11° of the Sun. Seen only in twilight, or not at all. It was largest just when it was hardest to see.
- **No eclipse.** Theia never crossed the Sun. Its closest pass, 8°, was far wider than its disk.
- **The impact was late afternoon.** At contact Theia was ~75° east of the Sun. The impact point was where it was about 5 p.m. local time, in hours of today's length. The proto-Earth day was shorter.
- These positions are measured from Earth's centre. In the last hour a surface observer's view shifts by up to ~12°.

## Earth from Theia

Earth was the inner planet. From Theia it behaved like Venus does for us, then grew into a full disk at midnight.

| Before impact | Where | Size | Brightness | Lit |
|---|---|---|---|---|
| 12–11 mo | Evening star, 84° then 60° east of the Sun | 2.2–2.5′ | mag −6 to −7 | 51 → 30% |
| 10 mo | Lost near the Sun, 21° east | 3.1′ | mag −3.3 | thin crescent, 4% |
| 9–6 mo | Morning star, climbing away from the Sun, 28° then 75° west | 2.4 → 1.0′ | mag −4 to −5 | 7 → 51% |
| 5–3 mo | 84° then 107° west | 1.0–1.5′ | mag −5 to −6.5 | 59 → 73% |
| 2–1 mo | 124° then 147° west | 2.4 → 5.5′ | mag −8 to −10 | 82 → 93% |
| Last 3 wk | High in the night sky, near opposition, 156° then 172° from the Sun | 8′ to 52′ | mag −11 to −15 | 96 → 100% |
| Last day | Opposite the Sun, then sliding toward it | 2.2° to 22° | mag −17 to −22 | full |

The two views mirror each other. From Earth, Theia was a thin crescent beside the Sun, seen at dusk or not at all. From Theia, Earth was a huge, full disk at midnight, swelling night by night. Through a telescope: dark rock, the white of the steam atmosphere's clouds, and any open water.

## The final weeks

From the run. Modeled, not published. Tide is tidal acceleration over surface gravity, in units of today's Moon on today's Earth.

| Before impact | Theia from Earth | Earth from Theia | Tide on Earth | Tide on Theia |
|---|---|---|---|---|
| 2 wk | 7′ | 12′ | 0.015 | 0.13 |
| 1 wk | 14′ | 24′ | 0.11 | 0.9 |
| 5 d | 19′ | 33′ | 0.3 | 2.4 |
| 3 d | 29′ | 52′ | 1.1 | 9 |
| 1 d | 1.3° | 2.2° | 19 | 160 |
| 12 hr | 2.2° | 3.8° | 100 | 840 |
| 6 hr | 3.7° | 6.5° | 490 | 4,100 |
| 1 hr | 13° | 22° | 20,000 | 170,000 |

Thresholds, Theia from Earth:
- **Brighter than any star:** already a year out.
- **A point again:** 8–3 months out, below 1′ as it swung away.
- **Clearly a disk:** ~1 month out, ~3′. But by then a thin crescent 31° from the Sun.
- **Larger than the Moon:** ~2.8 days out, 8° from the Sun, in the glare.
- **Growing while you watch:** ~2 hr out, most of a Moon-width every 5 minutes. Last ~15 min, minute to minute. This was the first time most of the day side could see it clearly, clear of the Sun and huge.

From Theia every threshold came earlier.

**The last normal day.** Both bodies were in free fall. The only felt signal was tides. The proto-Earth probably had no moon; its baseline tide was the Sun's.
- **Earth, ~3 days out.** Theia's tide matches today's lunar tide.
- 1 day out: ~20×. Metres to tens of metres in shallow basins, if there were oceans. *Estimate.*
- 12 hr out: ~100×. Solid ground flexing tens of metres a cycle. Quakes and eruptions likely rise. *Estimate.*
- Last hour: the bulge reaches kilometres.
- **Theia, ~7 days out.** It felt ~8× Earth's tidal stress throughout and broke from normal first.

See `./context.md` and `./timeline.csv`.

## The decades before

From `history_run.py`. Same contact state, integrated backward 3,000 years, then forward from earlier epochs with small errors. One plane (A-013). Modeled, not published.

**Close passes.** Theia's orbit is more stretched than the gap between the orbits. Near each conjunction it loops past Earth about once a year, several times over. Over 3,000 years: 30 passes inside one mutual Hill radius (1.5 million km). Median interval 46 years, about one per conjunction (A-014). Range 6–555 years.

**The last deep pass.** 53.4 years before contact, at 1.06 million km (0.71 Hill radii). It moved Theia from just inside Earth's orbit to 0.013 AU outside it, which set the ~48-year cadence that ends in the hit. Before it, 55–80 years out, the two had nearly the same orbit size, years within a day of each other, and passed within 1.2–2.4 million km four times.

**When the hit becomes certain.** Forward runs, 40 per epoch, Theia known to 1 km and 1 mm/s.

| Years before | Still hits | Contact angle, 5–95% |
|---|---|---|
| 1 | 100% | 44.8–45.2° |
| 5 | 100% | 44.9–45.1° |
| 10 | 100% | 43.7–46.3° |
| 20 | 100% | 41.5–49.3° |
| 30 | 100% | 38.3–53.7° |
| 50 | 100% | 34.9–60.0° |
| 53 | 100% | 34.8–55.8° |
| 54 | 20% | 7.5–71.6° |
| 80 | 2% | — |
| 100 | 0% | — |

- The hit is certain from the deep pass at 53.4 years. Half a year before it, it is not.
- From ~100 years out, rounding error alone changes the outcome.
- Angle within ±1°: ~5 years out. The spread does not shrink smoothly; it depends on where in the yearly loop the errors start.

**Unseen planetesimal hits on Theia,** at ~10 km/s:
- 10 km: no effect.
- 30 km: ±0.7° at 10 years, ±6° at 50.
- 100 km: 10 years out, 90% still hit, anywhere from 24° to 78°. Even 1 year out, ±4.5°.

The angle locks at ~5–10 years only if every body above ~30 km is accounted for.

**Merger.** From 53 years in, 90% of hits land at 35–60°. At 9.5 km/s that is inside the merge zone at any angle (Genda, Kokubo & Ida 2012).

**Limits.** One plane, so deep passes come more often than with tilted orbits (A-013). Point masses. No other planets or planetesimals. One approach direction. Ranges from 40 runs.
