"""Detailed Radxa enclosure assembly with non-printable reference hardware."""

import importlib.util
from pathlib import Path


def load_detailed_assembly():
    path = Path(__file__).with_name("radxa_modular_foldable_enclosure_visual.step.py")
    spec = importlib.util.spec_from_file_location("radxa_detailed_assembly", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def gen_step():
    assembly = load_detailed_assembly().gen_step()
    assembly.label = "radxa_enclosure_detailed_assembly"
    return assembly
