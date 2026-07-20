---
name: districts-batch4-method
description: Reusable fetch deltas confirmed in the districts fan-out batch 4 (NYSED instid endpoint, elementary Census geo, OSC field, parcel-district gate)
metadata:
  type: reference
---

Batch 4 of the Nassau districts data fan-out (PR #16, 2026-07-20, 13/13 complete).
Output-only files: `.claude/scratch/fanout/batch-4.json` + `batch-4-provenance.md`.
Extends [[districts-data-sourcing]]. Method deltas that worked and are reusable:

- **NYSED instid lookup** = `https://data.nysed.gov/search_schools.php?term=<name>`
  (JSON autocomplete, `source:"/search_schools.php"` in the homepage JS). Filter
  `type=="16"` for the district. Search is FUZZY — "Westbury" returns East Meadow
  + East Williston UFSD first; match on the returned `value` name, not position.
  (Coordinator's alt: `lists.php?type=district&start=<ASCII letter>`.)
- **Census elementary districts use `9500000US<geoid>`** (sumlevel 950), NOT
  9700000US (970=unified) or 9600000US (960=secondary). Applied to Floral
  Park-Bellerose + Valley Stream 24. Unified districts resolve directly at
  9700000US — no place proxy needed.
- **OSC levy field is `school_district_tax_levy`** (per `municipality` segment);
  sum segments for multi-town districts (FPB, Jericho, North Shore, Westbury).
- **Parcel-district HARD GATE:** GIS layer 1 has no district field, so confirm the
  discovered parcel via the LRV `/info/<PARID>/` page "School District: NAME - n"
  label AND the STAR-savings line matching the DTF exempt-savings figure to the
  dollar. This caught a Malverne-*addressed* parcel actually in another district
  (hamlet name != school district).
- **GIS point query needs 300-500 m radius** (60 m often returns zero features).
- **City districts (Glen Cove, like Long Beach pilot)** assess their own roll: the
  county LRV gstaxes returns "located within the City of..." with NO school lines.
  schoolRate/libraryRate OMITTED with a `schoolRateScope` note; levy still from OSC.
- **Elementary parcels** show ONE combined Net School Tax line (elem + CHSD billed
  together), not separable; record as combined + note. OSC levy is elementary-only.
- **Structural library-line absence** (East Rockaway, Malverne, Mineola, North
  Shore) is a real omission, not a fetch miss — libraryRate omitted with a note.
