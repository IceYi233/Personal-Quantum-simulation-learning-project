# Learning Notes

This file records the learning process, development boundaries, and engineering decisions behind this two-qubit Hamiltonian simulation project.

The project is a compact exercise in quantum simulation and scientific Python. It implements the same physical model in two forms:

- direct NumPy/SciPy matrix-exponential evolution
- Qiskit circuit construction with statevector simulation

## Project Snapshot

The simulated Hamiltonian is:

```text
H = J Z0Z1 + h(X0 + X1)
```

with:

- `J = 1.0`
- `h = 0.5`
- initial states `|00>`, `|01>`, `|10>`, and `|11>`
- time grid `np.linspace(0, 10, 200)`
- observables `<Z0>`, `<Z1>`, and `<Z0Z1>`

The completed project scope is NumPy exact simulation plus Qiskit statevector circuit simulation. It intentionally does not include Qiskit Aer backends, noise models, shot-based execution, real hardware execution, or Trotter error analysis.

## What This Project Demonstrates

The project shows how to:

- define a two-qubit spin-chain Hamiltonian
- represent quantum states as statevectors
- compute exact time evolution using a matrix exponential
- calculate expectation values for single-qubit and two-qubit observables
- reproduce the same dynamics using a Qiskit circuit representation
- validate the Qiskit result against a direct matrix-exponential reference
- save generated plots for each initial state

The NumPy implementation is the reference calculation because it directly evaluates:

```text
U(t) = exp(-iHt)
```

The Qiskit implementation expresses the same Hamiltonian dynamics as a circuit using `SparsePauliOp`, `PauliEvolutionGate`, and `Statevector`.

## Repository Contents

The repository is organized around a small reproducible workflow:

- `scripts/Two_qubit_Numpy_evolution.py`: builds the Pauli matrices, Hamiltonian, exact evolution operator, expectation values, numerical checks, and NumPy output plots
- `scripts/Two_qubit_Qiskit_circuit.py`: builds the Qiskit Hamiltonian, circuit evolution, statevector simulation, exact reference comparison, numerical checks, and Qiskit output plots
- `figures/Numpy_Simulation/`: stores PNG outputs from the NumPy script
- `figures/Qiskit_Simulation/`: stores PNG outputs from the Qiskit script
- `requirements.txt`: lists the Python dependencies used by the project
- `environment.yml`: defines a Conda environment entry point that installs from `requirements.txt`
- `README.md`: provides the main public-facing project description
- `LEARNING_NOTES.md`: documents the learning process, AI-assistance boundaries, and engineering takeaways

## Validation Approach

The main validation goal is not only to produce plots, but also to verify that the implementations are numerically consistent.

Both scripts use a tolerance of `1e-10`.

The NumPy script checks:

- statevector norm preservation for each initial state
- symmetry between `<Z0>` and `<Z1>` for the aligned initial states `|00>` and `|11>`
- swap symmetry between the anti-aligned initial states `|01>` and `|10>`

The Qiskit script checks the same properties and also compares the circuit statevector results against a direct matrix-exponential reference for `<Z0>`, `<Z1>`, and `<Z0Z1>` across all four initial states.

The expected success messages are:

```text
Numerical checks passed.
Qiskit circuit numerical checks passed.
```

These checks make the project more than a plotting script: they provide a clear numerical link between the exact reference implementation and the Qiskit implementation.

## AI-Assisted Development Boundaries

AI assistance was used in a limited and explicit way. In this project, AI refers to OpenAI Codex.

The AI-assisted parts were:

- generating and modifying the NumPy exact simulation code
- generating and modifying the Qiskit statevector simulation code
- helping construct the initial project structure and documentation framework

The author completed the remaining work independently:

- learning the required background concepts in Hamiltonian time evolution, statevectors, expectation values, Pauli operators, and Qiskit circuit representation
- deciding the final project scope: NumPy exact simulation plus Qiskit statevector simulation
- deciding not to include Aer, noise models, shot-based execution, real hardware execution, or Trotter analysis in the completed scope
- reviewing, revising, and finalizing the documentation content
- checking that the README and learning notes matched the actual repository behavior
- reviewing, testing, and editing the AI-assisted code and project structure
- creating and managing the Git repository
- performing Git commits, uploads, and repository publication or sharing steps

The author takes responsibility for the final implementation, results, documentation, and repository content.

## Author Work and Engineering Skills Demonstrated

This project demonstrates that the author can turn a small scientific computing goal into a structured and reproducible repository.

The author's work included understanding the physical model, interpreting the Hamiltonian terms, connecting the matrix-based NumPy reference with the Qiskit circuit representation, and ensuring that the generated outputs matched the intended simulation scope.

The project demonstrates several practical engineering abilities:

- translating a mathematical model into executable scientific code
- separating an exact reference implementation from a second implementation used for comparison
- using numerical checks rather than relying only on visual plots
- managing dependencies through `requirements.txt` and `environment.yml`
- keeping unused dependencies, such as `qiskit-aer`, out of the final environment
- organizing source scripts, generated figures, and documentation clearly
- documenting scope limits so future readers know what is included and what is not
- using Git to manage, commit, and upload the project
- using AI assistance transparently while retaining author review and responsibility

## Scope Control

A key engineering decision was to keep the completed scope small and verifiable.

The project does not attempt to include every possible Qiskit feature. Instead, it focuses on one complete workflow:

```text
NumPy exact result -> Qiskit statevector result -> numerical comparison -> plots
```

This makes the project easier to review, reproduce, and extend later.

## Possible Local Extensions

The following extensions are possible on a local development machine, but are not part of the completed project scope:

- Trotter error analysis for comparing exact evolution with product-formula approximations
- parameter sweeps over different `J`, `h`, and total evolution time
- extension from two qubits to small spin chains
- additional observables, such as entanglement entropy or state fidelity

## Final Scope

The completed scope is NumPy exact simulation plus Qiskit statevector simulation. The project provides a reference result, reproduces it with Qiskit circuits, validates the numerical agreement, and records the workflow in a reproducible repository.
