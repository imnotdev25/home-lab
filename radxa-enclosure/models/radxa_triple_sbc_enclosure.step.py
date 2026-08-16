"""Parametric Radxa triple-SBC enclosure.

Units: millimetres.
Origin: enclosure footprint centre on the bottom plane; +Z is upward.

The model is a printable base, lid, filter-retainer frame, and mounting pads.
The boards and the 5010 fan are intentionally represented by the documented
envelopes in the comments/parameters, not included in the printable STL.
"""

from build123d import Align, Box, Compound, Cylinder, Pos
from cadgen.assembly import label_shape


# ---- enclosure envelope -------------------------------------------------
OUTER_W = 108.0
OUTER_D = 78.0
WALL = 2.4
BOTTOM = 3.0
BASE_H = 86.0
LID_T = 3.0
LID_LIP_H = 6.0

PCB_T = 1.6
BOARD_HOLE_INSET = 4.0
M3_CLEAR = 3.4

# Hardware intent: F-F 15 mm and M-F 25 mm nylon M3 spacers.
FF_SPACER = 15.0
MF_SPACER = 25.0

# Board envelopes from Radxa documentation; Z positions are derived from the
# actual spacer stack so a hardware change updates every support and dummy.
A5E_Z = BOTTOM + FF_SPACER
A7A_Z = A5E_Z + PCB_T + MF_SPACER
ZERO3E_Z = A7A_Z + PCB_T + FF_SPACER
BOARDS = (
    ("cubie_a5e", 69.0, 56.0, A5E_Z),
    ("cubie_a7a", 85.0, 56.0, A7A_Z),
    ("radxa_zero_3e", 65.0, 30.0, ZERO3E_Z),
)

# Mounting-hole half-pitches. ZERO 3E uses its own smaller 57.8 x 22.9 mm
# pattern (measured from Radxa's V1.2 PCBA STEP); do not reuse Cubie spacing.
BOARD_HOLE_OFFSETS = {
    "cubie_a5e": (30.5, 24.0),
    "cubie_a7a": (38.5, 24.0),
    "radxa_zero_3e": (28.9, 11.45),
}


def board_hole_points(name):
    hx, hy = BOARD_HOLE_OFFSETS[name]
    return ((-hx, -hy), (hx, -hy), (-hx, hy), (hx, hy))

# 5010 fan and removable cloth-filter interface.
FAN_W = 50.0
FAN_OPENING = 46.0
FAN_HOLE_SPACING = 40.0
FILTER_OUTER = 60.0
FILTER_INNER = FAN_OPENING
FILTER_FRAME_H = 2.0


def cuboid(w: float, d: float, h: float, z: float = 0.0):
    return Pos(0, 0, z) * Box(w, d, h, align=(Align.CENTER, Align.CENTER, Align.MIN))


def ring(outer_w: float, outer_d: float, inner_w: float, inner_d: float, h: float, z: float):
    return cuboid(outer_w, outer_d, h, z) - cuboid(inner_w, inner_d, h + 0.4, z - 0.2)


def through_box(w: float, d: float, h: float, x: float, y: float, z: float):
    return Pos(x, y, z) * Box(w, d, h, align=(Align.CENTER, Align.CENTER, Align.MIN))


def through_cylinder(radius: float, h: float, x: float, y: float, z: float):
    return Pos(x, y, z) * Cylinder(radius, h, align=(Align.CENTER, Align.CENTER, Align.MIN))


def board_mount_pads():
    """Small wall-connected pads with M3 clearance holes at each PCB level."""
    pads = []
    inner_x = OUTER_W / 2 - WALL
    for name, board_w, board_d, board_z in BOARDS:
        pad_z = board_z - 2.0
        for x, y in board_hole_points(name):
                pad = through_box(14.0, 14.0, 2.0, x, y, pad_z)
                # Bridge the outer x pads into the side wall so they print as
                # attached features instead of unsupported islands.
                if abs(x) > 30.0:
                    bridge_x = -1 if x < 0 else 1
                    bridge = through_box(8.0, 14.0, 2.0, bridge_x * (inner_x - 4.0), y, pad_z)
                    pad = pad + bridge
                pad = pad - through_cylinder(M3_CLEAR / 2, 3.0, x, y, pad_z - 0.5)
                pads.append(label_shape(pad, "m3_board_mount", name, f"x{x:g}_y{y:g}"))
    return pads


def make_base():
    base = cuboid(OUTER_W, OUTER_D, BASE_H)
    cavity = cuboid(OUTER_W - 2 * WALL, OUTER_D - 2 * WALL, BASE_H, BOTTOM)
    base = base - cavity

    # Rear Ethernet cutouts: one service window at each board level. The
    # windows are deliberately generous because RJ45 positions vary by SKU.
    for _, _, _, board_z in BOARDS:
        base = base - through_box(50.0, 6.0, 16.0, 0, OUTER_D / 2, board_z + 1.0)

    # Three USB-C power/data service slots on the left side.
    for _, _, _, board_z in BOARDS:
        base = base - through_box(7.0, 20.0, 10.0, -OUTER_W / 2, -10.0, board_z - 1.0)

    # Controlled exhaust grille low on the front wall. Fan intake is through
    # the filtered lid; these slots establish a downward airflow path.
    for x in (-30, -18, -6, 6, 18, 30):
        base = base - through_box(4.0, 6.0, 20.0, x, -OUTER_D / 2, 8.0)

    # Corner lid bosses with M3 pilot/clearance holes.
    for x in (-47.0, 47.0):
        for y in (-32.0, 32.0):
            boss = through_cylinder(4.5, BASE_H - BOTTOM, x, y, BOTTOM)
            boss = boss - through_cylinder(2.2, BASE_H, x, y, 0)
            base = base + boss

    for pad in board_mount_pads():
        base = base + pad
    return label_shape(base, "enclosure_base", "sealed_air_plenum")


def make_lid():
    lid_z = BASE_H
    lid = cuboid(OUTER_W, OUTER_D, LID_T, lid_z)
    lip = ring(OUTER_W - 2 * WALL - 0.8, OUTER_D - 2 * WALL - 0.8,
               OUTER_W - 2 * WALL - 5.0, OUTER_D - 2 * WALL - 5.0,
               LID_LIP_H, lid_z - LID_LIP_H)
    lid = lid + lip

    # Filtered fan inlet, four 40 mm fan mounting holes, and a shallow gasket/
    # cloth-seating recess around the inlet.
    lid = lid - through_box(FAN_OPENING, FAN_OPENING, LID_T + 2.0, 0, 0, lid_z - 0.5)
    for x in (-FAN_HOLE_SPACING / 2, FAN_HOLE_SPACING / 2):
        for y in (-FAN_HOLE_SPACING / 2, FAN_HOLE_SPACING / 2):
            lid = lid - through_cylinder(1.7, LID_T + 2.0, x, y, lid_z - 0.5)

    gasket = ring(64.0, 64.0, 58.0, 58.0, 1.1, lid_z + LID_T - 1.1)
    lid = lid - gasket

    for x in (-47.0, 47.0):
        for y in (-32.0, 32.0):
            lid = lid - through_cylinder(2.2, LID_T + LID_LIP_H + 2.0, x, y, lid_z - LID_LIP_H - 0.5)
    return label_shape(lid, "enclosure_lid", "filtered_fan_cover")


def make_filter_retainer():
    frame = ring(FILTER_OUTER, FILTER_OUTER, FILTER_INNER, FILTER_INNER, FILTER_FRAME_H, BASE_H + LID_T)
    for x in (-FAN_HOLE_SPACING / 2, FAN_HOLE_SPACING / 2):
        for y in (-FAN_HOLE_SPACING / 2, FAN_HOLE_SPACING / 2):
            frame = frame - through_cylinder(1.7, FILTER_FRAME_H + 1.0, x, y, BASE_H + LID_T - 0.5)
    return label_shape(frame, "cloth_filter_retainer", "50mm_fan_filter")


def make_internal_air_guide():
    """Short square guide under the fan; leaves the board stack unobstructed."""
    guide = ring(58.0, 58.0, FAN_OPENING, FAN_OPENING, 10.0, BASE_H - 7.0)
    return label_shape(guide, "fan_air_guide", "downward_cpu_draft")


def gen_step():
    children = [make_base(), make_lid(), make_filter_retainer(), make_internal_air_guide()]
    return Compound(children=children, label="radxa_triple_sbc_enclosure")
