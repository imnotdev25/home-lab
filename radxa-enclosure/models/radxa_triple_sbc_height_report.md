# Radxa triple-SBC enclosure height check

All dimensions are millimetres. Z=0 is the outside bottom of the enclosure.

| Item | Bottom Z | Top Z | Height / gap |
|---|---:|---:|---:|
| Stabilizing base plinth | 0.0 | 3.0 | 120 × 90 × 3.0 |
| A5E PCB plane | 18.0 | 19.6 | 1.6 PCB |
| A7A underside-heatsink envelope | 36.6 | 44.6 | 8.0 below PCB |
| A7A PCB plane | 44.6 | 46.2 | 1.6 PCB |
| ZERO 3E PCB plane | 61.2 | 62.8 | 1.6 PCB |
| 5010 fan | 76.0 | 86.0 | 50×50×10 |
| Lid underside / top | 86.0 / 89.0 | — | 3.0 lid |
| Cloth-filter retainer top | — | 91.5 | 2.5 frame |

Spacer checks:

- Base → A5E: 18.0 − 3.0 = 15.0 mm F-F spacer.
- A5E → A7A: 44.6 − 19.6 = 25.0 mm M-F spacer.
- A7A 8 mm underside-heatsink envelope starts at Z=36.6, leaving
  36.6 − 19.6 = 17.0 mm above the A5E PCB. The A7A tray has a 64 × 42 mm
  central opening, so it does not obstruct that heatsink footprint.
- A7A → ZERO 3E: 61.2 − 46.2 = 15.0 mm F-F spacer.
- ZERO 3E nominal PCB top → fan underside: 76.0 − 62.8 = 13.2 mm airflow clearance,
  before any user-installed heatsink.
- Fan top meets the lid underside at Z=86.0.

Modular mount checks:

- Four flush base M3 pads are centred at the A5E pattern: ±30.5 × ±24.0 mm.
- The detachable wall body remains 108 × 78 mm; the base is widened to a
  120 × 90 mm rectangle with a 6 mm stabilizing overhang on every side.
- Each pad is 18 × 18 mm with a 3.4 mm M3 clearance hole and a 5 mm perimeter
  beyond the A5E board edge.
- ZERO 3E uses its separate small-pitch pattern: ±28.9 × ±11.45 mm
  (57.8 × 22.9 mm pitch), based on the official V1.2 PCBA STEP.
- Panel fasteners are modelled as M3×10 mm maximum; the printed panels remain
  separate solids and can be printed flat and detached individually.
- Reduced 4 mm-wide side rails begin 4.5 mm beyond the A7A board edge, leaving
  the requested 4 mm side clearance for a protruding SD card.

The board and connector dummy bodies were removed from the current visualization.
Confirm the actual heatsink/connector heights and board revision before final printing.
