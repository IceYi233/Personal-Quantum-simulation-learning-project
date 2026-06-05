# Learning Notes

This project is a compact learning exercise for two-qubit Hamiltonian time evolution. It focuses on building the same physical model in two representations:

- direct NumPy/SciPy matrix-exponential evolution
- Qiskit circuit construction with statevector simulation

## What This Project Demonstrates

The project shows how to define a two-qubit Hamiltonian, choose computational-basis initial states, evolve each state over time, calculate expectation values, and visualize the resulting dynamics.

The NumPy implementation is the reference calculation because it directly evaluates:

```text
U(t) = exp(-iHt)
```

The Qiskit implementation expresses the same Hamiltonian dynamics as a circuit using `SparsePauliOp`, `PauliEvolutionGate`, and `Statevector`.

## Validation Approach

The main validation goal is not only to produce plots, but also to verify that both implementations are numerically consistent.

The scripts check statevector norm preservation and expected symmetry relationships between the four initial states. The Qiskit script also compares the circuit statevector results against the direct matrix-exponential reference for the measured observables.

## AI-Assisted Development

OpenAI Codex was used as an assistant during documentation and repository polish. The assistance included reviewing README clarity, checking that `qiskit-aer` was not required by the current code, and refining the project description for a public or portfolio-style presentation.

The important technical behavior remains reproducible from the source code:

- dependencies are listed in `requirements.txt`
- the Conda entry point is listed in `environment.yml`
- the numerical validation checks are implemented in the scripts
- generated figures are saved under `figures/`

## Final Scope

The completed scope is NumPy exact simulation plus Qiskit statevector simulation. The project intentionally does not include Aer backends, noise simulation, shot-based measurements, or Trotter error analysis.
