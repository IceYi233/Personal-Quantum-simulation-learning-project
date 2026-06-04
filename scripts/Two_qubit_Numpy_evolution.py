import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm
from pathlib import Path

# Pauli matrices
I = np.array([[1, 0], [0, 1]], dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

# Tensor product helper
def kron(a, b):
    return np.kron(a, b)

# Two-qubit operators
X0 = kron(X, I)
X1 = kron(I, X)
Z0 = kron(Z, I)
Z1 = kron(I, Z)
Z0Z1 = kron(Z, Z)

# Hamiltonian: H = J Z0Z1 + h(X0 + X1)
J = 1.0
h = 0.5
H = J * Z0Z1 + h * (X0 + X1)

initial_states = {
    "|00>": np.array([1, 0, 0, 0], dtype=complex),
    "|01>": np.array([0, 1, 0, 0], dtype=complex),
    "|10>": np.array([0, 0, 1, 0], dtype=complex),
    "|11>": np.array([0, 0, 0, 1], dtype=complex),
}

output_dir = Path(__file__).resolve().parent.parent / "figures" / "Numpy_Simulation"
output_dir.mkdir(parents=True, exist_ok=True)
plt.rcParams["savefig.directory"] = str(output_dir)

times = np.linspace(0, 10, 200)
tol = 1e-10
simulation_results = {}
figures_to_save = []


def assert_close(values, expected, check_name):
    values = np.asarray(values)
    expected = np.asarray(expected)
    max_error = np.max(np.abs(values - expected))
    assert max_error < tol, f"{check_name} failed: max error = {max_error:.3e}"


for state_label, psi0 in initial_states.items():
    z0_values = []
    z1_values = []
    zz_values = []
    norm_values = []

    for t in times:
        U = expm(-1j * H * t)
        psi_t = U @ psi0
        norm_values.append(np.linalg.norm(psi_t))

        ev_Z0 = np.vdot(psi_t, Z0 @ psi_t).real
        ev_Z1 = np.vdot(psi_t, Z1 @ psi_t).real
        ev_ZZ = np.vdot(psi_t, Z0Z1 @ psi_t).real

        z0_values.append(ev_Z0)
        z1_values.append(ev_Z1)
        zz_values.append(ev_ZZ)

    simulation_results[state_label] = {
        "z0": np.array(z0_values),
        "z1": np.array(z1_values),
        "zz": np.array(zz_values),
        "norm": np.array(norm_values),
    }

for state_label, result in simulation_results.items():
    assert_close(result["norm"], 1.0, f"Norm check for {state_label}")

for state_label in ("|00>", "|11>"):
    z0_minus_z1 = simulation_results[state_label]["z0"] - simulation_results[state_label]["z1"]
    assert_close(z0_minus_z1, 0.0, f"<Z0> - <Z1> symmetry check for {state_label}")

assert_close(
    simulation_results["|01>"]["z0"],
    simulation_results["|10>"]["z1"],
    "<Z0> for |01> and <Z1> for |10> swap symmetry check",
)
assert_close(
    simulation_results["|01>"]["z1"],
    simulation_results["|10>"]["z0"],
    "<Z1> for |01> and <Z0> for |10> swap symmetry check",
)
print("Numerical checks passed.")

for state_label, result in simulation_results.items():
    fig, ax = plt.subplots()
    manager = getattr(fig.canvas, "manager", None)
    if manager is not None and hasattr(manager, "set_window_title"):
        manager.set_window_title(f"Initial state {state_label}, J=1.0, h=0.5")

    ax.plot(times, result["z0"], label="<Z0>", linestyle="--")
    ax.plot(times, result["z1"], label="<Z1>", alpha=0.6)
    ax.plot(times, result["zz"], label="<Z0Z1>")
    ax.set_xlabel("time")
    ax.set_ylabel("expectation value")
    ax.set_title(f"Two-qubit spin-chain time evolution from {state_label}")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()

    state_bits = state_label.strip("|>")
    figures_to_save.append((fig, output_dir / f"Initial_{state_bits}_expvl.png"))

for fig, output_path in figures_to_save:
    fig.savefig(output_path, dpi=200)
    print(f"Saved {output_path}")

plt.show()
