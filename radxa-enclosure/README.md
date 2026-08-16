# Radxa triple-SBC modular enclosure

Modular, screw-together enclosure for one Radxa Cubie A5E, one Radxa Cubie
A7A, one Radxa ZERO 3E, and a 5 V 5010 fan. It keeps Ethernet on the rear,
USB-C access on the left, and filters the fan intake before air reaches the
boards.

## Enclosure structure

```text
top:    5010 fan lid + cloth-filter retainer
        ──────────────────────────────────
upper:  Radxa ZERO 3E removable tray
middle: Radxa Cubie A7A removable tray
lower:  Radxa Cubie A5E on 15 mm nylon spacers
base:   120 × 90 × 3 mm stabilizing plinth
```

The four walls, fan lid, trays, and filter retainer are individual printed
parts. M3 bolts and nylon nuts let the walls and lid be removed without
breaking the enclosure apart.

- Ethernet openings face the rear wall.
- Three USB-C openings face the left wall.
- The right wall allows approximately 4 mm of SD-card clearance.
- The A7A tray has a 64 × 42 mm underside opening for its heatsink.
- The A5E-to-A7A PCB clearance is 25 mm; this leaves about 17 mm after the
  A7A's 8 mm underside heatsink.
- Install the fan to blow through the filter and downward toward the SBC CPUs;
  front-wall slots provide the outlet path.

## Bill of materials

### Printed parts

| Qty | Part |
|---:|---|
| 1 | Stabilizing base plinth |
| 1 | Front wall |
| 1 | Rear wall |
| 1 | Left wall |
| 1 | Right wall |
| 1 | A5E tray |
| 1 | A7A tray |
| 1 | ZERO 3E tray |
| 1 | Fan lid |
| 1 | Cloth-filter retainer |

### Electronics and airflow

| Qty | Component | Notes |
|---:|---|---|
| 1 | Radxa Cubie A5E | Lower SBC |
| 1 | Radxa Cubie A7A | Middle SBC; supplies the fan header |
| 1 | Radxa ZERO 3E | Upper SBC |
| 1 | 5 V 5010 axial fan | 50 × 50 × 10 mm |
| 1 | Cloth dust-filter media | Cut to approximately 52 × 52 mm |

### Nylon M3 hardware

| Qty | Component | Use |
|---:|---|---|
| 16 | M3 × 10 nylon bolts | Wall/lid joints |
| 16 | M3 nylon hex nuts | Wall/lid joints |
| 4 | M3 × 15 female-to-female nylon spacers | Base-to-A5E mounting |
| 8 | M3 × 10 nylon bolts | A5E base/spacer connections |
| 8 | M3 × 10 nylon bolts | A7A and ZERO 3E tray mounting |
| 8 | M3 nylon hex nuts | A7A and ZERO 3E tray mounting |
| 4 | M3 × 10 fan screws | Fan/filter/lid stack |

M3 × 25 male-to-female spacers are not required by this tray-supported
revision. Do not force direct board stacking: the Cubie mounting patterns
differ. For a fan with a cut USB lead, verify the A7A fan-header voltage,
pinout, and fan polarity before connecting it.

## Files and printing

```text
exports/
├── print-ready/          Individual STL and STEP files; slice these parts.
├── assembly-reference/   Multi-body assembly files and detailed BOM.
└── previews/             Local render images.
models/                   Parametric CAD project source.
```

Import the ten individual files in `exports/print-ready/` separately. Do not
import the multi-body STL/3MF files in `exports/assembly-reference/` as a
single printable model.

Suggested FDM settings: PETG or ASA, 0.20 mm layers, four perimeters, and
30–40% infill. Use supports only if your slicer identifies a local overhang;
the individual files are already placed with a flat build-plate face.

More export guidance is in [exports/README.md](exports/README.md), and the
full reference BOM is in
[exports/assembly-reference/radxa_enclosure_detailed_bom.md](exports/assembly-reference/radxa_enclosure_detailed_bom.md).
