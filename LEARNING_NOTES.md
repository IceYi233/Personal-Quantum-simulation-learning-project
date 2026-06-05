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

## AI-Assisted Development Boundaries

OpenAI Codex was used as an assistant in a limited and explicit way. The AI-assisted parts were:

- generating and modifying the NumPy exact simulation code
- generating and modifying the Qiskit statevector simulation code
- helping set up the initial project structure and documentation framework

The following parts were completed by the project author:

- learning the required background concepts in Hamiltonian time evolution, statevectors, expectation values, and Qiskit circuit representation
- deciding the final project scope: NumPy exact simulation plus Qiskit statevector simulation, without Aer, noise models, shot-based execution, or real hardware
- reviewing, revising, and finalizing the documentation content
- checking that the repository explanation matched the actual code behavior
- creating and managing the Git repository
- performing Git commits, uploads, and repository publication or sharing steps

The important technical behavior remains reproducible from the source code:

- dependencies are listed in `requirements.txt`
- the Conda entry point is listed in `environment.yml`
- the numerical validation checks are implemented in the scripts
- generated figures are saved under `figures/`

## Author Work and Engineering Skills Demonstrated

This project demonstrates that the author can turn a small scientific computing goal into a structured, reproducible repository.

The author's work included understanding the physical model, interpreting the Hamiltonian terms, connecting the matrix-based NumPy reference with the Qiskit circuit representation, and checking that the generated outputs matched the intended simulation scope.

The project also shows several practical engineering abilities:

- environment management with `requirements.txt` and `environment.yml`
- clear separation between source scripts, generated figures, and documentation
- validation-oriented development through numerical tolerance checks
- dependency scope control by excluding unused packages such as `qiskit-aer`
- documentation suitable for project review, portfolio presentation, or future continuation
- Git-based project organization and publication workflow

## Final Scope

The completed scope is NumPy exact simulation plus Qiskit statevector simulation. The project intentionally does not include Aer backends, noise simulation, shot-based measurements, or Trotter error analysis.
