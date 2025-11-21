from typing import Tuple

from guppylang import guppy
from guppylang.std.builtins import owned, result
from guppylang.std.quantum import (
    cx,
    h,
    measure,
    qubit,
    x,
    z,
)


# --- Quantum program (from official Guppy teleportation example) ---


@guppy
def teleport(src: qubit @ owned, tgt: qubit) -> None:
    """Teleports the state in `src` to `tgt`."""
    tmp = qubit()
    h(tmp)
    cx(tmp, tgt)
    cx(src, tmp)

    h(src)
    if measure(src):
        z(tgt)
    if measure(tmp):
        x(tgt)


@guppy
def teleport_one_state() -> None:
    """
    Prepare |1>, teleport it, and report the result as a classical bit.
    This is executed on the Selene-backed emulator under the hood.
    """
    src = qubit()
    tgt = qubit()

    # Prepare |1> state on src
    x(src)
    teleport(src, tgt)

    result("teleported", measure(tgt))


def run_quantum_demo(shots: int = 1) -> Tuple[str, int, int, dict]:
    """
    Run the Guppy program on the emulator and return:
    - quantum_sample: string description of the measurement
    - quantum_shots: how many shots were run (demo uses 1)
    - qaoa_iterations: 0 (we're not actually optimising QAOA params yet)
    - metadata: raw entries from QsysShot for transparency
    """
    # As per docs: .emulator(...).stabilizer_sim().with_seed(...).run()
    # Selene is used under the hood by Guppy’s emulator. :contentReference[oaicite:0]{index=0}
    emu = teleport_one_state.emulator(n_qubits=3).stabilizer_sim().with_seed(2)
    sim_result = emu.run()  # single shot is fine for demo

    shots_list = list(sim_result.results)
    if not shots_list:
        return "no_result", 0, 0, {}

    shot = shots_list[0]
    # QsysShot(entries=[('teleported', 1)]) in the teleport example. :contentReference[oaicite:1]{index=1}
    try:
        entries = getattr(shot, "entries", [])
    except Exception:
        entries = []

    if entries:
        key, value = entries[0]
        sample_str = f"{key}={value}"
    else:
        sample_str = "unknown"

    metadata = {"entries": entries}

    return sample_str, shots, 0, metadata
