from pathlib import Path
import warnings

import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp, Statevector
from scipy.linalg import expm
from scipy.sparse import SparseEfficiencyWarning


warnings.filterwarnings("ignore", category=SparseEfficiencyWarning)


# Model parameters for H = J Z0Z1 + h(X0 + X1)
J = 1.0
h = 0.5

# Qiskit Pauli labels follow the same displayed basis order used here:
# "ZI" acts on the left qubit in |q0 q1>, and "IZ" acts on the right qubit.
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

TIMES = np.linspace(0, 10, 200)
TOL = 1e-10
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "figures" / "Qiskit_Simulation"


def computational_basis_circuit(state_bits):
    circuit = QuantumCircuit(2)
    for qubit_index, bit in enumerate(reversed(state_bits)):
        if bit == "1":
            circuit.x(qubit_index)
    return circuit


def evolution_circuit(state_bits, time):
    circuit = computational_basis_circuit(state_bits)
    circuit.append(PauliEvolutionGate(HAMILTONIAN, time=time), [0, 1])
    return circuit


def exact_hamiltonian_matrix():
    return HAMILTONIAN.to_matrix()


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


def simulate_exact_matrix_reference():
    hamiltonian = exact_hamiltonian_matrix()
    results = {}

    for state_label, state_bits in INITIAL_STATES.items():
        psi0 = Statevector.from_label(state_bits).data
        z0_values = []
        z1_values = []
        zz_values = []

        for time in TIMES:
            psi_t = expm(-1j * hamiltonian * time) @ psi0
            state = Statevector(psi_t)
            z0_values.append(expectation_value(state, OBSERVABLES["z0"]))
            z1_values.append(expectation_value(state, OBSERVABLES["z1"]))
            zz_values.append(expectation_value(state, OBSERVABLES["zz"]))

        results[state_label] = {
            "z0": np.array(z0_values),
            "z1": np.array(z1_values),
            "zz": np.array(zz_values),
        }

    return results


def run_numerical_checks(qiskit_results, exact_results):
    for state_label, result in qiskit_results.items():
        assert_close(result["norm"], 1.0, f"Norm check for {state_label}")

    for state_label, result in qiskit_results.items():
        for observable_name in ("z0", "z1", "zz"):
            assert_close(
                result[observable_name],
                exact_results[state_label][observable_name],
                f"Qiskit vs exact check for {state_label} {observable_name}",
            )

    for state_label in ("|00>", "|11>"):
        z0_minus_z1 = qiskit_results[state_label]["z0"] - qiskit_results[state_label]["z1"]
        assert_close(z0_minus_z1, 0.0, f"<Z0> - <Z1> symmetry check for {state_label}")

    assert_close(
        qiskit_results["|01>"]["z0"],
        qiskit_results["|10>"]["z1"],
        "<Z0> for |01> and <Z1> for |10> swap symmetry check",
    )
    assert_close(
        qiskit_results["|01>"]["z1"],
        qiskit_results["|10>"]["z0"],
        "<Z1> for |01> and <Z0> for |10> swap symmetry check",
    )


def save_figures(results):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for state_label, result in results.items():
        fig, ax = plt.subplots()
        manager = getattr(fig.canvas, "manager", None)
        if manager is not None and hasattr(manager, "set_window_title"):
            manager.set_window_title(f"Qiskit circuit initial state {state_label}, J=1.0, h=0.5")

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
        output_path = OUTPUT_DIR / f"Initial_{state_bits}_expvl.png"
        fig.savefig(output_path, dpi=200)
        print(f"Saved {output_path}")

    if plt.get_backend().lower() != "agg":
        plt.show()
    else:
        plt.close("all")


def main():
    qiskit_results = simulate_qiskit_circuits()
    exact_results = simulate_exact_matrix_reference()
    run_numerical_checks(qiskit_results, exact_results)
    print("Qiskit circuit numerical checks passed.")
    save_figures(qiskit_results)


if __name__ == "__main__":
    main()
