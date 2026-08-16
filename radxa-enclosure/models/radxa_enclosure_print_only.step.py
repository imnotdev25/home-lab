"""Print-only Radxa enclosure: all and only manufactured plastic components."""

import importlib.util
from pathlib import Path


def load_printable_assembly():
    path = Path(__file__).with_name("radxa_modular_foldable_enclosure.step.py")
    spec = importlib.util.spec_from_file_location("radxa_printable_assembly", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def gen_step():
    assembly = load_printable_assembly().gen_step()
    assembly.label = "radxa_enclosure_print_only"
    return assembly
