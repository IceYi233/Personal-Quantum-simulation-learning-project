# Learning Notes

This file records the learning process and conceptual understanding behind this two-qubit Hamiltonian simulation project. It focuses on what was learned and how the model is understood, rather than on Git or repository-management details.

The project implements the same physical model in two forms:

- direct NumPy/SciPy matrix-exponential evolution
- Qiskit circuit construction with statevector simulation

## Learning Goal

The main learning goal was to understand a complete small-scale quantum simulation workflow:

- how a Hamiltonian defines the dynamics of a quantum system
- how a two-qubit state can be represented as a statevector
- how time evolution is calculated from `exp(-iHt)`
- how expectation values connect the evolved state to observable quantities
- how the same dynamics can be represented in Qiskit using circuits and Pauli operators
- how to check that two implementations are describing the same physics

This project was intentionally kept small so that every step could be inspected directly. With only two qubits, the statevector has four components and the Hamiltonian is a `4x4` matrix, which makes the model suitable for learning and verification.

## Model Understanding

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

My understanding of each term is:

- `Z0Z1` describes interaction between the two qubits. It distinguishes aligned states from anti-aligned states in the computational basis.
- `X0 + X1` describes a transverse field acting on each qubit. Since `X` flips computational-basis states, this term drives nontrivial time evolution instead of leaving the basis states fixed.
- `J` controls the interaction strength, while `h` controls the transverse-field strength.

The model is symmetric under exchanging qubit 0 and qubit 1. This symmetry explains why `|01>` and `|10>` produce related curves with `<Z0>` and `<Z1>` interchanged.

## NumPy Exact Simulation Understanding

The NumPy implementation is the reference calculation. It directly constructs:

- Pauli matrices `I`, `X`, `Y`, and `Z`
- tensor-product operators such as `X0`, `X1`, `Z0`, `Z1`, and `Z0Z1`
- the Hamiltonian matrix `H`
- the time-evolution operator

The core calculation is:

```text
U(t) = exp(-iHt)
psi(t) = U(t) psi(0)
```

This helped me connect the mathematical formula for quantum time evolution with executable scientific Python code. It also made clear why NumPy/SciPy is useful as a reference: for a two-qubit system, the full matrix calculation is small, direct, and numerically reliable.

## Qiskit Statevector Simulation Understanding

The Qiskit implementation represents the same Hamiltonian dynamics in circuit form. It uses:

- `SparsePauliOp` to define the Hamiltonian and observables
- `PauliEvolutionGate` to express time evolution as a circuit operation
- `Statevector` to simulate the resulting circuit state

This stage helped me understand the difference between a matrix-based simulation and a circuit-based simulation. The Qiskit version still runs on a classical computer, but it expresses the model using objects closer to quantum-circuit language.

The important idea is that Qiskit is not used here for noisy hardware-style execution. It is used to reproduce the same statevector dynamics in a circuit representation.

## Observables and Plot Interpretation

The project calculates three observables:

- `<Z0>(t)`: the Z-direction expectation value of qubit 0
- `<Z1>(t)`: the Z-direction expectation value of qubit 1
- `<Z0Z1>(t)`: a two-qubit correlation observable

These observables make the state evolution easier to interpret. Instead of only looking at the full statevector, the plots show how measurable quantities change over time.

The initial value of `<Z0Z1>` separates aligned and anti-aligned states:

- `|00>` and `|11>` start with `<Z0Z1> = +1`
- `|01>` and `|10>` start with `<Z0Z1> = -1`

During evolution, the transverse-field term causes the expectation values to oscillate. The plotted curves therefore show both the interaction structure and the effect of the transverse field.

## Validation Understanding

The main validation goal is not only to produce plots, but to show that the two implementations agree numerically.

Both scripts use a tolerance of `1e-10`.

The checks include:

- statevector norm preservation
- symmetry between `<Z0>` and `<Z1>` for `|00>` and `|11>`
- swap symmetry between `|01>` and `|10>`
- Qiskit-vs-matrix-reference agreement for `<Z0>`, `<Z1>`, and `<Z0Z1>`

The Qiskit script compares its circuit statevector result with a direct matrix-exponential reference. This is the most important numerical check because it verifies that the circuit representation is reproducing the same Hamiltonian dynamics as the exact reference implementation.

The expected success messages are:

```text
Numerical checks passed.
Qiskit circuit numerical checks passed.
```

This validation step helped me understand that a useful simulation project should not rely only on visual plots. It should also contain explicit checks that can fail when the implementation is inconsistent.

## AI-Assisted Development Boundaries

AI assistance was used in a limited and explicit way. The AI-assisted parts were:

- generating and modifying the NumPy exact simulation code
- generating and modifying the Qiskit statevector simulation code
- constructing the initial project structure and documentation framework

The following work was completed by the author:

- learning the background concepts needed to understand Hamiltonian time evolution, statevectors, expectation values, Pauli operators, and Qiskit circuit representation
- deciding the completed scope of the project
- reviewing, testing, and editing the AI-assisted code
- interpreting the output plots and numerical checks
- revising and finalizing the documentation content
- deciding which dependencies and future extensions were appropriate for this local project

Version-control setup and upload were completed by the author, but they are not the main focus of these learning notes. The focus here is on conceptual understanding, implementation review, and validation.

The author takes responsibility for the final implementation, results, documentation, and repository content.

## Learning and Understanding Demonstrated

This project demonstrates the author's ability to:

- understand a compact quantum physics model and explain the role of each Hamiltonian term
- connect mathematical time evolution with concrete NumPy/SciPy code
- understand how Qiskit represents Pauli operators, evolution gates, and statevectors
- use an exact reference implementation to validate a second implementation
- reason about symmetry as a correctness check
- interpret expectation-value plots rather than treating them as black-box output
- limit project scope to a reproducible and verifiable result
- use AI-generated code critically by reviewing, testing, editing, and documenting it

The project therefore demonstrates both learning of the underlying quantum-simulation concepts and practical understanding of how to turn those concepts into a working computational workflow.

## Scope Control

A key learning outcome was understanding why the project should remain focused.

The completed scope is:

```text
NumPy exact result -> Qiskit statevector result -> numerical comparison -> plots
```

The project intentionally does not include Qiskit Aer backends, noise models, shot-based execution, real hardware execution, or Trotter error analysis in the completed version. Excluding these topics keeps the project easier to verify and makes the learning outcome clearer.

## Possible Local Extensions

The following extensions are possible on a local development machine, but are not part of the completed project scope:

- Trotter error analysis for comparing exact evolution with product-formula approximations
- parameter sweeps over different `J`, `h`, and total evolution time
- extension from two qubits to small spin chains
- additional observables, such as entanglement entropy or state fidelity

## Final Summary

This project shows a complete learning path from a simple Hamiltonian model to two working simulations and numerical validation. The NumPy implementation provides the exact reference result, while the Qiskit implementation reproduces the same dynamics through statevector circuit simulation.
