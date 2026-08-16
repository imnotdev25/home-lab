"""Detachable plate-and-wall Radxa SBC enclosure.

The printable assembly is intentionally panelized: base plate, four walls,
three removable SBC trays, lid, and filter retainer. Panels are not fused so
they can be printed flat and attached/detached with M3 hardware.
"""

import importlib.util
from pathlib import Path

from build123d import Align, Box, Compound, Cylinder, Pos
from cadgen.assembly import label_shape


def load_stack_parameters():
    path = Path(__file__).with_name("radxa_triple_sbc_enclosure.step.py")
    spec = importlib.util.spec_from_file_location("radxa_stack_parameters", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


E = load_stack_parameters()

OUTER_W = E.OUTER_W
OUTER_D = E.OUTER_D
BASE_OVERHANG = 6.0
BASE_W = OUTER_W + 2 * BASE_OVERHANG
BASE_D = OUTER_D + 2 * BASE_OVERHANG
BOTTOM_T = 3.0
PANEL_T = 3.0
WALL_Z = 3.0
WALL_H = 83.0
TOP_Z = WALL_Z + WALL_H
LID_T = 3.0
TRAY_T = 2.4
M3_CLEAR = 3.4
M3_MAX_LENGTH = 10.0
# A5E hole inset is 4 mm from the 69x56 mm board envelope on both axes;
# 18 mm pads therefore leave a true 5 mm perimeter beyond the board edge.
BASE_PAD_SIZE = 18.0
BASE_PAD_EDGE_MARGIN = 5.0
FAN_OPENING = 46.0
FAN_HOLE_SPACING = 40.0
FILTER_OUTER = 66.0
FILTER_INNER = 52.0
USB_SLOT_WIDTH = 26.0
USB_SLOT_HEIGHT = 12.0
A7A_UNDERSIDE_HEATSINK_H = 8.0
A7A_TRAY_OPENING_W = 64.0
A7A_TRAY_OPENING_D = 42.0
SD_CARD_SIDE_ALLOWANCE = 4.0
SIDE_RAIL_W = 4.0

# Eight perimeter fasteners let the walls be detached independently while
# keeping every screw at the requested maximum 10 mm length.
PANEL_FASTENER_POINTS = (
    (-47.0, -32.0), (47.0, -32.0), (-47.0, 32.0), (47.0, 32.0),
    (-32.0, -32.0), (32.0, -32.0), (-32.0, 32.0), (32.0, 32.0),
)


def block(w, d, h, x=0.0, y=0.0, z=0.0):
    return Pos(x, y, z) * Box(w, d, h, align=(Align.CENTER, Align.CENTER, Align.MIN))


def hole(radius, h, x, y, z):
    return Pos(x, y, z) * Cylinder(radius, h, align=(Align.CENTER, Align.CENTER, Align.MIN))


def cut_vertical_holes(shape, points, z, h=4.0):
    for x, y in points:
        shape = shape - hole(M3_CLEAR / 2, h, x, y, z)
    return shape


def make_base_plate():
    # A 6 mm overhang on each side forms a wide, rectangular stabilizing plinth
    # without changing the detachable 108 x 78 mm wall footprint.
    plate = block(BASE_W, BASE_D, BOTTOM_T)
    plate = cut_vertical_holes(plate, PANEL_FASTENER_POINTS, -0.5, BOTTOM_T + 1.0)
    # The four A5E M3 mounting surfaces are part of the plinth itself. Cutting
    # them through the base avoids overlapping solids in the print-only STL.
    plate = cut_vertical_holes(plate, E.board_hole_points("cubie_a5e"), -0.5, BOTTOM_T + 1.0)
    return label_shape(plate, "stabilizing_base_plinth",
                       "120x90mm_four_a5e_m3_mount_surfaces")


def wall_feet(side):
    if side in ("front", "back"):
        y = -32.0 if side == "front" else 32.0
        feet = block(OUTER_W - 10.0, 10.0, PANEL_T, y=y, z=WALL_Z)
        points = tuple((x, y) for x in (-47.0, -32.0, 32.0, 47.0))
    else:
        x = -47.0 if side == "left" else 47.0
        feet = block(10.0, OUTER_D - 10.0, PANEL_T, x=x, z=WALL_Z)
        points = tuple((x, y) for y in (-32.0, 32.0))
    return cut_vertical_holes(feet, points, WALL_Z - 0.5, PANEL_T + 1.0)


def shelf_rails(side):
    """Internal ledges that support trays while clearing a 4 mm SD-card overhang."""
    rails = []
    x = (-OUTER_W / 2 + PANEL_T + SIDE_RAIL_W / 2
         if side == "left" else OUTER_W / 2 - PANEL_T - SIDE_RAIL_W / 2)
    # The widest board is the 85 mm A7A: board edge ±42.5, rail inner edge
    # ±47.0. The resulting 4.5 mm gap accepts the requested 4 mm SD-card
    # overhang before the removable tray rail begins.
    assert OUTER_W / 2 - PANEL_T - SIDE_RAIL_W - max(board[1] for board in E.BOARDS) / 2 >= SD_CARD_SIDE_ALLOWANCE
    for _, _, _, board_z in E.BOARDS:
        tray_z = board_z - TRAY_T
        rail = block(SIDE_RAIL_W, OUTER_D - 16.0, 3.0, x=x, z=tray_z)
        rail = cut_vertical_holes(rail, ((x, -28.0), (x, 28.0)), tray_z - 0.5, 4.0)
        rails.append(rail)
    return rails


def make_wall(side):
    if side == "front":
        y = -OUTER_D / 2 + PANEL_T / 2
        wall = block(OUTER_W, PANEL_T, WALL_H, y=y, z=WALL_Z)
        for x in (-30, -18, -6, 6, 18, 30):
            wall = wall - block(4.0, 6.0, 20.0, x=x, y=-OUTER_D / 2, z=8.0)
    elif side == "back":
        y = OUTER_D / 2 - PANEL_T / 2
        wall = block(OUTER_W, PANEL_T, WALL_H, y=y, z=WALL_Z)
        # All three Ethernet connectors exit through the rear (+Y) wall.
        for _, _, _, board_z in E.BOARDS:
            wall = wall - block(50.0, 6.0, 16.0, y=OUTER_D / 2, z=board_z + 1.0)
    elif side == "left":
        x = -OUTER_W / 2 + PANEL_T / 2
        wall = block(PANEL_T, OUTER_D - 2 * PANEL_T, WALL_H, x=x, z=WALL_Z)
        # One enlarged USB-C access window per SBC, all on the left (-X).
        for _, _, _, board_z in E.BOARDS:
            wall = wall - block(6.0, USB_SLOT_WIDTH, USB_SLOT_HEIGHT,
                                 x=-OUTER_W / 2, y=-10.0,
                                 z=board_z - 1.0)
    else:
        x = OUTER_W / 2 - PANEL_T / 2
        wall = block(PANEL_T, OUTER_D - 2 * PANEL_T, WALL_H, x=x, z=WALL_Z)

    wall = wall + wall_feet(side)
    for rail in shelf_rails("left" if side == "left" else "right") if side in ("left", "right") else []:
        wall = wall + rail
    return label_shape(wall, f"modular_{side}_wall", "detachable_panel")


def make_partition_tray(name, board_w, board_d, board_z):
    tray_z = board_z - TRAY_T
    # Broad edge frame supports the PCB while the centre opening keeps each CPU
    # in the fan draft. The A7A opening is enlarged for its 8 mm underside
    # heatsink: the 25 mm A5E-to-A7A M3 spacer leaves 17 mm of free air above
    # the A5E PCB, and no tray material occupies the heatsink footprint.
    opening_w, opening_d = (A7A_TRAY_OPENING_W, A7A_TRAY_OPENING_D) if name == "cubie_a7a" else (58.0, 38.0)
    tray = block(OUTER_W - 2 * PANEL_T, OUTER_D - 2 * PANEL_T, TRAY_T, z=tray_z)
    tray = tray - block(opening_w, opening_d, TRAY_T + 1.0, z=tray_z - 0.5)
    board_holes = (
        *E.board_hole_points(name),
    )
    tray = cut_vertical_holes(tray, board_holes, tray_z - 0.5, TRAY_T + 1.0)
    return label_shape(tray, f"partition_{name}_tray", "removable_sbc_plate")


def make_lid():
    lid = block(OUTER_W, OUTER_D, LID_T, z=TOP_Z)
    lid = lid - block(FAN_OPENING, FAN_OPENING, LID_T + 1.0, z=TOP_Z - 0.5)
    for x in (-FAN_HOLE_SPACING / 2, FAN_HOLE_SPACING / 2):
        for y in (-FAN_HOLE_SPACING / 2, FAN_HOLE_SPACING / 2):
            lid = lid - hole(1.7, LID_T + 1.0, x, y, TOP_Z - 0.5)
    lid = cut_vertical_holes(lid, PANEL_FASTENER_POINTS, TOP_Z - 0.5, LID_T + 1.0)
    return label_shape(lid, "modular_lid_plate", "m3x10_wall_fasteners")


def make_filter_retainer():
    outer = block(FILTER_OUTER, FILTER_OUTER, 2.5, z=TOP_Z + LID_T)
    inner = block(FILTER_INNER, FILTER_INNER, 3.5, z=TOP_Z + LID_T - 0.5)
    frame = outer - inner
    for x in (-FAN_HOLE_SPACING / 2, FAN_HOLE_SPACING / 2):
        for y in (-FAN_HOLE_SPACING / 2, FAN_HOLE_SPACING / 2):
            frame = frame - hole(1.7, 3.5, x, y, TOP_Z + LID_T - 0.5)
    return label_shape(frame, "cloth_filter_retainer", "removable_filter_frame")


def make_components():
    components = [make_base_plate()]
    components.extend(make_wall(side) for side in ("front", "back", "left", "right"))
    components.extend(
        make_partition_tray(name, width, depth, board_z)
        for name, width, depth, board_z in E.BOARDS
    )
    components.extend((make_lid(), make_filter_retainer()))
    return components


def gen_step():
    return Compound(children=make_components(), label="radxa_modular_foldable_enclosure")
