# Two-Qubit Spin-Chain Time Evolution

## Project Goal

This project simulates the time evolution of a two-qubit spin-chain model. The first stage uses NumPy and SciPy to perform exact statevector simulation. Later stages will translate the same model into Qiskit circuits and compare exact evolution with Trotterized circuit evolution.

The main goal is to build a small but complete quantum simulation workflow:

- define a Hamiltonian
- choose initial quantum states
- compute time evolution
- calculate expectation values
- plot and interpret the results
- later reproduce the same model using Qiskit

## Model

The Hamiltonian used in the current stage is

```text
H = J Z0Z1 + h(X0 + X1)
```

where:

- `Z0Z1` describes the interaction between the two qubits
- `X0 + X1` describes the transverse field acting on both qubits
- `J = 1.0` is the interaction strength
- `h = 0.5` is the transverse-field strength

The exact time evolution is calculated as

```text
|psi(t)> = exp(-iHt)|psi(0)>
```

The current observables are:

- `<Z0>(t)`: expectation value of qubit 0 in the Z direction
- `<Z1>(t)`: expectation value of qubit 1 in the Z direction
- `<Z0Z1>(t)`: two-qubit correlation observable

## Stage 1: NumPy Exact Simulation

### Reason to Start with NumPy

Although the final goal of this project is to simulate the model using Qiskit, the NumPy simulation provides an exact reference result for the Qiskit simulation later.

In the NumPy stage, the two-qubit quantum state is represented directly as a four-dimensional statevector. The Hamiltonian is represented as a `4x4` matrix, and the time-evolution operator is computed directly as:

```text
U(t) = exp(-iHt)
```

This is the standard matrix-based form of quantum time evolution. For a two-qubit system, the matrix is small enough that this exact calculation is straightforward and reliable.

The Qiskit stage then implements the same Hamiltonian dynamics using a quantum-circuit representation. In this project, Qiskit is still run on a classical computer simulator, but it expresses the time evolution in terms of quantum gates and circuits rather than direct matrix exponentiation.

Therefore, the NumPy result is used as the reference answer:

- NumPy gives the exact matrix-exponential result.
- Qiskit translates the same time evolution into a circuit-based simulation.
- Later Trotterized circuits can be compared against the NumPy exact result to measure approximation error.

In short, the NumPy stage answers what the Qiskit simulation should reproduce.

### Construction

The NumPy version directly constructs the Pauli matrices, tensor-product operators, Hamiltonian matrix, and time-evolution operator. It then evaluates the expectation values for four computational-basis initial states:

- `|00>`
- `|01>`
- `|10>`
- `|11>`

The current script is:

```text
scripts/Two_qubit_Numpy_evolution.py
```

The output figures are saved in:

```text
figures/Numpy_Simulation
```

### Results

#### Initial State `|00>`

![Initial state |00>](figures/Numpy_Simulation/Initial_00_expvl.png)

#### Initial State `|01>`

![Initial state |01>](figures/Numpy_Simulation/Initial_01_expvl.png)

#### Initial State `|10>`

![Initial state |10>](figures/Numpy_Simulation/Initial_10_expvl.png)

#### Initial State `|11>`

![Initial state |11>](figures/Numpy_Simulation/Initial_11_expvl.png)

### Observations

For the symmetric Hamiltonian `H = J Z0Z1 + h(X0 + X1)`, the dynamics is invariant under the exchange of qubit 0 and qubit 1. Therefore, the initial states `|01>` and `|10>` give symmetric expectation-value curves, with `<Z0>` and `<Z1>` interchanged.

The observable `<Z0Z1>` measures the correlation between the two qubits. It starts from `+1` for the aligned states `|00>` and `|11>`, and from `-1` for the anti-aligned states `|01>` and `|10>`. During the time evolution, `<Z0Z1>` oscillates while preserving the qualitative distinction between initially aligned and anti-aligned configurations in this parameter setting.

## Stage 2: Qiskit Circuit Simulation

The Qiskit version reproduces the same Hamiltonian dynamics using Qiskit circuits, `PauliEvolutionGate`, `SparsePauliOp`, and statevector simulation.

The current script is:

```text
scripts/Two_qubit_Qiskit_circuit.py
```

The output figures are saved in:

```text
figures/Qiskit_Simulation
```

This stage uses the same model, initial states, and observables as the NumPy exact simulation. The script also checks that the Qiskit circuit results match the direct matrix-exponential reference within numerical tolerance.

## Optional Future Work: Trotter Error Analysis

Trotter error analysis is not required for the current learning goal of this repository. It is a possible extension if I want to study how Hamiltonian time evolution can be approximated by splitting the evolution into smaller circuit steps.

The basic idea would be to compare the exact evolution

```text
exp[-i(A + B)t]
```

with a Trotterized approximation such as

```text
[exp(-iA t/r) exp(-iB t/r)]^r
```

where `r` is the number of Trotter steps. Increasing `r` usually makes the approximation closer to the exact result, but it also makes the circuit longer.

For this project, the Trotter stage would be a follow-up topic rather than part of the current completed scope.

## How to Run

This project should be run in a project-specific Python environment. PyCharm may use a different interpreter from the `python` command in a normal terminal, so always check which Python is active before running the script.

Recommended Python version:

```text
Python 3.11
```

### Option 1: Conda environment

Create the environment:

```bash
conda env create -f environment.yml
```

Activate it:

```bash
conda activate qclp-qiskit
```

Run the current NumPy simulation script:

```bash
python scripts/Two_qubit_Numpy_evolution.py
```

Run the Qiskit circuit simulation script:

```bash
python scripts/Two_qubit_Qiskit_circuit.py
```

### Option 2: Existing Python environment

If you already have a suitable Python environment, activate it first, then install the dependencies:

```bash
pip install -r requirements.txt
```

Run the current NumPy simulation script:

```bash
python scripts/Two_qubit_Numpy_evolution.py
```

Run the Qiskit circuit simulation script:

```bash
python scripts/Two_qubit_Qiskit_circuit.py
```

To check which Python is being used:

```bash
python -c "import sys; print(sys.executable)"
```

To check whether the required packages are installed:

```bash
python -c "import numpy, scipy, matplotlib, qiskit; print('environment ok')"
```

## Requirements

Current and planned project requirements:

- `numpy`
- `scipy`
- `matplotlib`
- `qiskit`
- `qiskit-aer`

The current NumPy stage only uses `numpy`, `scipy`, and `matplotlib`. The Qiskit packages are included now so the same environment can also run the upcoming circuit and Trotter stages.

## Next Steps

- Compare exact and Trotterized time evolution.
