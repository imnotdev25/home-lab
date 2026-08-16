"""Visualization-only modular enclosure with coloured dummy hardware."""

import importlib.util
from pathlib import Path

from build123d import (Align, Box, Color, Compound, Cylinder, Pos,
                       RegularPolygon, extrude)
from cadgen.assembly import label_shape


def load_modular():
    path = Path(__file__).with_name("radxa_modular_foldable_enclosure.step.py")
    spec = importlib.util.spec_from_file_location("radxa_modular_enclosure", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def block(w, d, h, x=0.0, y=0.0, z=0.0):
    return Pos(x, y, z) * Box(w, d, h, align=(Align.CENTER, Align.CENTER, Align.MIN))


def cylinder(radius, h, x, y, z):
    return Pos(x, y, z) * Cylinder(radius, h, align=(Align.CENTER, Align.CENTER, Align.MIN))


def nylon_nut(x, y, z):
    """M3 nylon hex nut envelope: 5.5 mm across flats, 2.4 mm thick."""
    outer = Pos(x, y, z) * extrude(
        RegularPolygon(3.2, 6, major_radius=True, rotation=30,
                       align=(Align.CENTER, Align.CENTER)),
        amount=2.4,
    )
    return outer - cylinder(1.6, 3.0, x, y, z - 0.3)


def dummy_bolt(label, x, y, z):
    """M3 bolt envelope with a low-profile head and 10 mm shaft."""
    shaft = cylinder(1.5, 10.0, x, y, z)
    head = cylinder(3.0, 1.8, x, y, z + 8.2)
    bolt = label_shape(shaft + head, "dummy_m3_bolt", label, "M3x10mm")
    bolt.color = Color(0.85, 0.55, 0.08)
    return bolt


def dummy_nut(label, x, y, z):
    nut = label_shape(nylon_nut(x, y, z), "dummy_m3_nylon_nut", label,
                      "M3_nylon_hex")
    nut.color = Color(0.92, 0.92, 0.92)
    return nut


def dummy_fan_5010(z):
    """Visual 5010 fan: square frame, open rotor, hub and blades.

    The USB lead is cut and terminated at the A7A fan header, so no external
    USB-A cutout is added to the enclosure.
    """
    frame = block(50.0, 50.0, 10.0, z=z)
    frame = frame - block(42.0, 42.0, 11.0, z=z - 0.5)
    frame = label_shape(frame, "dummy_5010_fan", "50x50x10mm_frame")
    frame.color = Color(0.10, 0.10, 0.10)
    hub = label_shape(cylinder(12.0, 6.0, 0.0, 0.0, z + 2.0),
                      "dummy_5010_fan", "rotor_hub")
    hub.color = Color(0.16, 0.16, 0.16)
    blade_a = label_shape(block(5.0, 22.0, 1.2, y=10.0, z=z + 5.0),
                          "dummy_5010_fan", "rotor_blade_a")
    blade_b = label_shape(block(22.0, 5.0, 1.2, x=10.0, z=z + 5.0),
                          "dummy_5010_fan", "rotor_blade_b")
    blade_a.color = Color(0.12, 0.12, 0.12)
    blade_b.color = Color(0.12, 0.12, 0.12)
    return (frame, hub, blade_a, blade_b)


def gen_step():
    m = load_modular()
    components = m.make_components()
    wall_color = Color(0.42, 0.48, 0.58)
    tray_color = Color(0.12, 0.35, 0.70)
    for part in components:
        if "partition_" in str(part.label):
            part.color = tray_color
        elif "base_m3_mount_surface" in str(part.label):
            part.color = Color(0.15, 0.65, 0.85)
        elif "cloth_filter" in str(part.label):
            part.color = Color(0.85, 0.70, 0.18)
        else:
            part.color = wall_color

    # Deliberately omit the SBC/connector dummy pads: the visualization now
    # shows only printable panels plus separate fan and mounting hardware.
    children = list(components)

    # Fan sits below the lid; the filter cloth sits above it in the removable
    # retainer pocket. Both are coloured separately from printed panels.
    cloth = label_shape(block(m.FILTER_INNER, m.FILTER_INNER, 0.4, z=m.TOP_Z + m.LID_T + 0.2),
                        "dummy_cloth_filter", "replaceable_filter_media")
    cloth.color = Color(0.75, 0.75, 0.75)
    children.extend(dummy_fan_5010(m.TOP_Z - 10.0))
    children.append(cloth)
    for x in (-m.FAN_HOLE_SPACING / 2, m.FAN_HOLE_SPACING / 2):
        for y in (-m.FAN_HOLE_SPACING / 2, m.FAN_HOLE_SPACING / 2):
            children.append(dummy_bolt("fan_filter_lid_screw", x, y,
                                       m.TOP_Z + m.LID_T + 2.5 - 10.0))

    # Coloured, non-printable M3 bolt + nylon hex-nut hardware for panel joints.
    for x, y in m.PANEL_FASTENER_POINTS:
        children.append(dummy_bolt("base_wall_joint", x, y, -2.0))
        children.append(dummy_nut("base_wall_joint_nut", x, y, 6.0))
        children.append(dummy_bolt("lid_wall_joint", x, y, m.TOP_Z - 10.0))
        children.append(dummy_nut("lid_wall_joint_nut", x, y, m.TOP_Z - 12.4))

    # First Cubie sits on four 15 mm female-to-female spacer envelopes. The
    # lower and upper M3x10 bolts engage each threaded end of each spacer.
    for index, (x, y) in enumerate(m.E.board_hole_points("cubie_a5e"), start=1):
        spacer = label_shape(cylinder(3.0, m.E.FF_SPACER, x, y, m.BOTTOM_T),
                             "dummy_m3_female_female_spacer", f"a5e_{index}", "15mm")
        spacer.color = Color(0.55, 0.18, 0.65)
        children.append(spacer)
        children.append(dummy_bolt("a5e_base_to_spacer_bolt", x, y, -7.0))
        children.append(dummy_bolt("a5e_board_bolt", x, y, 9.6))

    # The upper boards fasten directly to their removable trays with M3x10
    # bolts and nylon hex nuts; this is why the 25 mm M-F spacers are not
    # required in the plate-supported revision.
    for name, _, _, board_z in m.E.BOARDS:
        if name == "cubie_a5e":
            continue
        for x, y in m.E.board_hole_points(name):
            children.append(dummy_bolt(f"{name}_tray_bolt", x, y, board_z - 8.0))
            children.append(dummy_nut(f"{name}_tray_nut", x, y,
                                      board_z - m.TRAY_T - 2.4))

    return Compound(children=children, label="radxa_modular_foldable_enclosure_visual")
