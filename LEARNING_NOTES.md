# Learning Notes

This file records the learning process and conceptual understanding behind this two-qubit Hamiltonian simulation project. It focuses on what was learned and how the model is understood, rather than on Git or repository-management details.

The project implements the same physical model in two forms:

- direct NumPy/SciPy matrix-exponential evolution
- Qiskit circuit construction with statevector simulation

## Project Content

This project focuses on a small two-qubit Hamiltonian simulation. The main content includes:

- Hamiltonian-based time evolution for a two-qubit quantum system
- statevector representation of the four computational-basis states
- exact matrix-exponential simulation with NumPy/SciPy
- expectation-value calculation for single-qubit and two-qubit observables
- Qiskit statevector circuit simulation of the same model
- comparison between the matrix-based reference and the Qiskit circuit representation

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

The single-qubit computational basis states are `|0>` and `|1>`. For two qubits, the computational basis is:

```text
|00>, |01>, |10>, |11>
```

A general two-qubit state can be written as:

```text
|ψ> = a|00> + b|01> + c|10> + d|11>
```

where `a`, `b`, `c`, and `d` are complex amplitudes. The values `|a|^2`, `|b|^2`, `|c|^2`, and `|d|^2` are the probabilities of measuring the corresponding computational-basis states.

In a two-qubit system, single-qubit operators are extended to the four-dimensional state space using tensor products:

```text
Z0 = Z tensor I
Z1 = I tensor Z
X0 = X tensor I
X1 = I tensor X
Z0Z1 = Z tensor Z
```

Here `Z0` acts on the first qubit and `Z1` acts on the second qubit. Similarly, `X0` flips the first qubit and `X1` flips the second qubit.

My understanding of the Hamiltonian is that its two parts have different roles:

- `Z0Z1` defines the aligned and anti-aligned structure in the Z basis.
- `X0 + X1` drives amplitude flow among computational-basis states by flipping one qubit at a time.
- `J` controls the interaction strength, while `h` controls the transverse-field strength.

The action of `Z` on a single qubit is:

```text
Z|0> = +|0>
Z|1> = -|1>
```

Therefore, the `Z0Z1` term acts on the computational-basis states as:

```text
Z0Z1|00> = +|00>
Z0Z1|11> = +|11>
Z0Z1|01> = -|01>
Z0Z1|10> = -|10>
```

This means `|00>` and `|11>` are aligned states, while `|01>` and `|10>` are anti-aligned states. In this sense, `Z0Z1` can be understood as a Z-direction correlation operator.

The action of `X` on a single qubit is:

```text
X|0> = |1>
X|1> = |0>
```

For two-qubit case, it turns:

```text
X0|00> = |10>
X1|00> = |01>
(X0 + X1)|00> = |10> + |01>
```

This means that an initial amplitude in the `|00>` direction can flow into the `|10>` and `|01>` directions during time evolution. More generally, `X0 + X1` connects each computational-basis state to states that differ by flipping exactly one qubit.

The expectation values are used to read out the effect of this evolution in the Z basis:

- `<Z0>(t)` reflects whether the first qubit is biased toward `|0>` or `|1>`.
- `<Z1>(t)` reflects the same information for the second qubit.
- `<Z0Z1>(t)` indicates whether the two qubits are overall aligned or anti-aligned.

The model is symmetric under exchanging qubit 0 and qubit 1. This symmetry explains why `|01>` and `|10>` produce related curves with `<Z0>` and `<Z1>` interchanged.

## NumPy Exact Simulation Understanding

The NumPy implementation is the reference calculation. It directly constructs:

- Pauli matrices `I`, `X`, `Y`, and `Z`
- tensor-product operators such as `X0`, `X1`, `Z0`, `Z1`, and `Z0Z1`
- the Hamiltonian matrix `H`
- the time-evolution operator

The initial implementation was developed with AI assistance, then reviewed and revised while checking it against the mathematical form of the model.

The core calculation is:

```text
U(t) = exp(-iHt)
ψ(t) = U(t) ψ(0)
```

This helped me connect the mathematical formula for quantum time evolution with executable scientific Python code. It also made clear why NumPy/SciPy is useful as a reference: for a two-qubit system, the full matrix calculation is small, direct, and numerically reliable.

## Qiskit Statevector Simulation Understanding

The Qiskit implementation represents the same Hamiltonian dynamics in circuit form. It uses:

- `SparsePauliOp` to define the Hamiltonian and observables
- `PauliEvolutionGate` to express time evolution as a circuit operation
- `Statevector` to simulate the resulting circuit state

The Qiskit implementation was also developed with AI assistance, then reviewed against the NumPy reference and the intended project scope.

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

## Scope Control

The project keeps the completed scope focused on one small and verifiable workflow.

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

## Summary

This project shows a complete learning path from a simple Hamiltonian model to two working simulations and numerical validation. The NumPy implementation provides the exact reference result, while the Qiskit implementation reproduces the same dynamics through statevector circuit simulation.
