from pathlib import Path
import warnings

import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit.synthesis import MatrixExponential
from scipy.sparse import SparseEfficiencyWarning

if __package__:
    from .two_qubit_numpy_matrix import simulate_numpy_matrix
else:
    from two_qubit_numpy_matrix import simulate_numpy_matrix


# Model parameters for H = J Z0Z1 + h(X0 + X1)
J = 1.0
h = 0.5

# Qiskit Pauli labels are ordered by circuit qubits as |q1 q0>.
# This project calls the left logical qubit q0 and the right logical qubit q1,
# so "ZI" is project Z0 and "IZ" is project Z1.
HAMILTONIAN = SparsePauliOp.from_list(
    [
        ("ZZ", J),
        ("XI", h),
        ("IX", h),
    ]
)

OBSERVABLES = {
    "z0": SparsePauliOp.from_list([("ZI", 1.0)]),
    "z1": SparsePauliOp.from_list([("IZ", 1.0)]),
    "zz": SparsePauliOp.from_list([("ZZ", 1.0)]),
}

INITIAL_STATES = {
    "|00>": "00",
    "|01>": "01",
    "|10>": "10",
    "|11>": "11",
}

EXPECTED_INITIAL_VALUES = {
    "|00>": {"z0": 1.0, "z1": 1.0, "zz": 1.0},
    "|01>": {"z0": 1.0, "z1": -1.0, "zz": -1.0},
    "|10>": {"z0": -1.0, "z1": 1.0, "zz": -1.0},
    "|11>": {"z0": -1.0, "z1": -1.0, "zz": 1.0},
}

TIMES = np.linspace(0, 10, 200)
TOL = 1e-10
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "figures" / "qiskit_circuit"


def computational_basis_circuit(state_bits):
    circuit = QuantumCircuit(2)
    # The project writes state bits from left to right as q0 q1, but Qiskit
    # circuit qubit 0 is the right-hand bit, so reverse the bits before mapping.
    for qubit_index, bit in enumerate(reversed(state_bits)):
        if bit == "1":
            circuit.x(qubit_index)
    return circuit


def evolution_circuit(state_bits, time):
    circuit = computational_basis_circuit(state_bits)
    evolution_gate = PauliEvolutionGate(
        HAMILTONIAN,
        time=time,
        synthesis=MatrixExponential(),
    )
    circuit.append(evolution_gate, [0, 1])
    return circuit


def assert_close(values, expected, check_name):
    values = np.asarray(values)
    expected = np.asarray(expected)
    max_error = np.max(np.abs(values - expected))
    assert max_error < TOL, f"{check_name} failed: max error = {max_error:.3e}"


def expectation_value(state, observable):
    return state.expectation_value(observable).real


def simulate_qiskit_circuits():
    results = {}

    for state_label, state_bits in INITIAL_STATES.items():
        z0_values = []
        z1_values = []
        zz_values = []
        norm_values = []

        for time in TIMES:
            circuit = evolution_circuit(state_bits, time)
            # Exact synthesis can emit harmless sparse-format efficiency warnings.
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore",
                    category=SparseEfficiencyWarning,
                    module=r"scipy\.sparse\.linalg\..*",
                )
                state = Statevector.from_instruction(circuit)

            norm_values.append(np.linalg.norm(state.data))
            z0_values.append(expectation_value(state, OBSERVABLES["z0"]))
            z1_values.append(expectation_value(state, OBSERVABLES["z1"]))
            zz_values.append(expectation_value(state, OBSERVABLES["zz"]))

        results[state_label] = {
            "z0": np.array(z0_values),
            "z1": np.array(z1_values),
            "zz": np.array(zz_values),
            "norm": np.array(norm_values),
        }

    return results


def run_numerical_checks(qiskit_results, numpy_results):
    for state_label, result in qiskit_results.items():
        assert_close(result["norm"], 1.0, f"Norm check for {state_label}")

    for state_label, expected_values in EXPECTED_INITIAL_VALUES.items():
        for observable_name, expected_value in expected_values.items():
            assert_close(
                qiskit_results[state_label][observable_name][0],
                expected_value,
                f"Initial {observable_name} check for {state_label}",
            )

    max_observable_error = 0.0
    for state_label, result in qiskit_results.items():
        for observable_name in ("z0", "z1", "zz"):
            numpy_values = numpy_results[state_label][observable_name]
            assert_close(
                result[observable_name],
                numpy_values,
                f"Qiskit vs NumPy check for {state_label} {observable_name}",
            )
            max_observable_error = max(
                max_observable_error,
                float(np.max(np.abs(result[observable_name] - numpy_values))),
            )

    # Aligned initial states: within-plot coincidence.
    for state_label in ("|00>", "|11>"):
        z0_minus_z1 = qiskit_results[state_label]["z0"] - qiskit_results[state_label]["z1"]
        assert_close(z0_minus_z1, 0.0, f"<Z0> - <Z1> symmetry check for {state_label}")

    # Aligned initial states: cross-plot sign reflection.
    for observable_name in ("z0", "z1"):
        assert_close(
            qiskit_results["|11>"][observable_name],
            -qiskit_results["|00>"][observable_name],
            f"Aligned cross-plot {observable_name} sign-reflection check for |11> and |00>",
        )

    # Anti-aligned initial states: within-plot sign reflection.
    for state_label in ("|01>", "|10>"):
        assert_close(
            qiskit_results[state_label]["z0"],
            -qiskit_results[state_label]["z1"],
            f"Anti-aligned within-plot <Z0> = -<Z1> check for {state_label}",
        )

    # Anti-aligned initial states: cross-plot sign reflection.
    for observable_name in ("z0", "z1"):
        assert_close(
            qiskit_results["|10>"][observable_name],
            -qiskit_results["|01>"][observable_name],
            f"Anti-aligned cross-plot {observable_name} sign-reflection check for |10> and |01>",
        )

    # Correlation curves coincide within the aligned and anti-aligned pairs.
    assert_close(
        qiskit_results["|00>"]["zz"],
        qiskit_results["|11>"]["zz"],
        "<Z0Z1> coincidence check for |00> and |11>",
    )
    assert_close(
        qiskit_results["|01>"]["zz"],
        qiskit_results["|10>"]["zz"],
        "<Z0Z1> coincidence check for |01> and |10>",
    )

    # Aligned and anti-aligned correlation curves are sign-reversed.
    assert_close(
        qiskit_results["|01>"]["zz"],
        -qiskit_results["|00>"]["zz"],
        "<Z0Z1> sign-reflection check for |01> and |00>",
    )
    assert_close(
        qiskit_results["|10>"]["zz"],
        -qiskit_results["|11>"]["zz"],
        "<Z0Z1> sign-reflection check for |10> and |11>",
    )

    print(
        f"Max Qiskit vs NumPy observable error: {max_observable_error:.3e} "
        f"(tolerance {TOL:.1e})"
    )


def save_figures(results):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for state_label, result in results.items():
        fig, ax = plt.subplots()
        manager = getattr(fig.canvas, "manager", None)
        if manager is not None and hasattr(manager, "set_window_title"):
            manager.set_window_title(f"Qiskit circuit initial state {state_label}, J={J}, h={h}")

        ax.axhline(y=0, color="black", linewidth=1.0)
        ax.set_ylim(-1.05, 1.05)

        ax.plot(TIMES, result["z0"], label="<Z0>", linestyle="--")
        ax.plot(TIMES, result["z1"], label="<Z1>", alpha=0.6)
        ax.plot(TIMES, result["zz"], label="<Z0Z1>")
        ax.set_xlabel("time")
        ax.set_ylabel("expectation value")
        ax.set_title(f"Qiskit circuit evolution from {state_label}")
        ax.legend()
        ax.grid(True)
        fig.tight_layout()

        state_bits = state_label.strip("|>")
        output_path = OUTPUT_DIR / f"Initial_{state_bits}_expvl_circuit.png"
        fig.savefig(output_path, dpi=200)
        print(f"Saved {output_path}")

    if plt.get_backend().lower() != "agg":
        plt.show()
    else:
        plt.close("all")


def main():
    qiskit_results = simulate_qiskit_circuits()
    numpy_results = simulate_numpy_matrix(J, h, TIMES)
    run_numerical_checks(qiskit_results, numpy_results)
    print("Qiskit circuit numerical checks passed.")
    save_figures(qiskit_results)


if __name__ == "__main__":
    main()
