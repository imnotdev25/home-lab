# Radxa triple-SBC enclosure — detailed component list

This bill of materials belongs with `radxa_enclosure_detailed_assembly.step`.
All dimensions are in millimetres.

## Printed parts — 10 bodies

| Qty | Part | Notes |
|---:|---|---|
| 1 | Stabilizing base plinth | 120 × 90 × 3; includes four A5E M3 mounting holes. |
| 1 | Front wall | Detachable; exhaust slots. |
| 1 | Rear wall | Detachable; all Ethernet access openings. |
| 1 | Left wall | Detachable; three USB-C access openings. |
| 1 | Right wall | Detachable; SD-card clearance side. |
| 1 | A5E tray | Removable SBC tray. |
| 1 | A7A tray | Removable; 64 × 42 heatsink clearance opening. |
| 1 | ZERO 3E tray | Removable; small-pitch M3 pattern. |
| 1 | Fan lid | 5010 mounting pattern and 46 mm airflow opening. |
| 1 | Cloth-filter retainer | 52 × 52 filter-media opening. |

## Purchased electronics and airflow parts

| Qty | Component | Notes |
|---:|---|---|
| 1 | Radxa Cubie A5E | Base SBC. |
| 1 | Radxa Cubie A7A | Middle SBC; use its fan header for the modified fan lead. |
| 1 | Radxa ZERO 3E | Upper SBC. |
| 1 | 5 V 5010 axial fan | 50 × 50 × 10; USB lead cut and terminated to the A7A fan header. |
| 1 | Cloth dust-filter media | Cut to approximately 52 × 52; held by the printed retainer. |

## M3 nylon hardware — current tray-supported revision

| Qty | Component | Use |
|---:|---|---|
| 16 | M3 × 10 nylon bolts | Eight base/wall and eight lid/wall joints. |
| 16 | M3 nylon hex nuts | Counterparts for the detachable wall/lid joints. |
| 4 | M3 × 15 female-to-female nylon spacers | Base to A5E mounting points. |
| 8 | M3 × 10 nylon bolts | Four base-to-spacer and four A5E-to-spacer fasteners. |
| 8 | M3 × 10 nylon bolts | Four A7A-tray and four ZERO-3E-tray board mounts. |
| 8 | M3 nylon hex nuts | Counterparts for A7A and ZERO-3E tray mounting. |
| 4 | M3 × 10 fan screws | Fan/filter/lid stack; use threaded fan bosses or self-tapping fan screws. |

## Spacer note

The panel-and-tray construction supports the A7A and ZERO 3E independently,
so M3 × 25 male-to-female spacers are **not structurally required** in this
revision. The 25 mm A5E-to-A7A clearance remains in the CAD. Directly stacking
the two Cubie boards with those spacers would require an adapter because their
M3 mounting patterns differ.
