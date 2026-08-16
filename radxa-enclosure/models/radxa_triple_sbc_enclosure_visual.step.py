"""Visualization assembly with dummy Radxa boards, connectors, spacers, and fan.

This file is for fit/height review only. Do not print it: the dummy electronics
and fan are included intentionally so the stack can be inspected in CAD Viewer.
"""

import importlib.util
from pathlib import Path

from build123d import Align, Box, Color, Compound, Cylinder, Pos
from cadgen.assembly import label_shape


def load_enclosure():
    path = Path(__file__).with_name("radxa_triple_sbc_enclosure.step.py")
    spec = importlib.util.spec_from_file_location("radxa_triple_sbc_enclosure", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def block(w, d, h, x=0, y=0, z=0):
    return Pos(x, y, z) * Box(w, d, h, align=(Align.CENTER, Align.CENTER, Align.MIN))


def cylinder(radius, h, x, y, z):
    return Pos(x, y, z) * Cylinder(radius, h, align=(Align.CENTER, Align.CENTER, Align.MIN))


def dummy_board(name, w, d, z, cpu_h=3.0, ethernet_count=1):
    board = label_shape(block(w, d, 1.6, z=z), name, "pcb_envelope")
    board.color = Color(0.08, 0.35, 0.12)

    cpu = label_shape(block(18.0, 18.0, cpu_h, z=z + 1.6), name, "cpu_heatsink_envelope")
    cpu.color = Color(0.85, 0.35, 0.08)

    parts = [board, cpu]
    # Generic connector envelopes: intentionally conservative for visualization.
    for index in range(ethernet_count):
        x = (index - (ethernet_count - 1) / 2) * 20.0
        rj45 = label_shape(block(18.0, 10.0, 13.5, x=x, y=d / 2 + 4.0, z=z + 1.6),
                           name, f"rj45_{index + 1}")
        rj45.color = Color(0.08, 0.08, 0.08)
        parts.append(rj45)

    usb_c = label_shape(block(10.0, 7.0, 4.0, x=-w / 2 - 2.0, y=-8.0, z=z + 1.6),
                        name, "usb_c_envelope")
    usb_c.color = Color(0.08, 0.08, 0.08)
    parts.append(usb_c)

    header = label_shape(block(48.0, 5.5, 8.0, x=0, y=-d / 2 + 5.0, z=z + 1.6),
                         name, "40pin_header_envelope")
    header.color = Color(0.08, 0.08, 0.08)
    parts.append(header)
    return parts


def spacer_pair(label, x, y, z, length):
    spacer = cylinder(3.0, length, x, y, z)
    return label_shape(spacer, "m3_nylon_spacer", label, f"{length:g}mm")


def gen_step():
    e = load_enclosure()
    children = [e.make_base(), e.make_lid(), e.make_filter_retainer(), e.make_internal_air_guide()]

    # These are the same board envelopes used by the enclosure supports.
    a5e, a7a, zero3e = e.BOARDS
    children.extend(dummy_board("dummy_cubie_a5e", a5e[1], a5e[2], a5e[3], ethernet_count=2))
    children.extend(dummy_board("dummy_cubie_a7a", a7a[1], a7a[2], a7a[3], ethernet_count=1))
    children.extend(dummy_board("dummy_radxa_zero_3e", zero3e[1], zero3e[2], zero3e[3], ethernet_count=1))

    # Hardware gaps: base→A5E = 15, A5E→A7A = 25, A7A→ZERO = 15 mm.
    for index, (length, z0, board_w, board_d) in enumerate((
        (e.FF_SPACER, e.BOTTOM, a5e[1], a5e[2]),
        (e.MF_SPACER, a5e[3] + e.PCB_T, a7a[1], a7a[2]),
        (e.FF_SPACER, a7a[3] + e.PCB_T, zero3e[1], zero3e[2]),
    ), start=1):
        for x in (-board_w / 2 + 4.0, board_w / 2 - 4.0):
            for y in (-board_d / 2 + 4.0, board_d / 2 - 4.0):
                children.append(spacer_pair(f"level_{index}", x, y, z0, length))

    # 5010 fan envelope: 50×50×10, mounted below the lid so filtered air is
    # drawn through the cloth filter and blown down through the board stack.
    fan = label_shape(block(50.0, 50.0, 10.0, z=76.0), "dummy_5010_fan", "50x50x10mm")
    fan.color = Color(0.12, 0.12, 0.12)
    children.append(fan)

    # Height assertions are deliberately explicit so a future spacer change
    # fails loudly instead of silently creating a collision.
    assert abs((a5e[3] - e.BOTTOM) - e.FF_SPACER) < 1e-6
    assert abs((a7a[3] - (a5e[3] + e.PCB_T)) - e.MF_SPACER) < 1e-6
    assert abs((zero3e[3] - (a7a[3] + e.PCB_T)) - e.FF_SPACER) < 1e-6
    assert 76.0 - (zero3e[3] + e.PCB_T + 3.0) > 10.0  # CPU to fan underside
    assert e.BASE_H - (76.0 + 10.0) == 0.0             # fan top meets lid underside

    return Compound(children=children, label="radxa_triple_sbc_enclosure_with_dummy_hardware")
