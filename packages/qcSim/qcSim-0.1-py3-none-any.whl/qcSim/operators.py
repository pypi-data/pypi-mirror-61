import numpy as np
import itertools


class Operator():

    """
    Instances of the operator class represent unitary quantum operators for single or multi-qubit systems.
    This class also contains some functions for creating specific quantum operators.
    """

    def __init__(self, matrix):
        """
        Creates a quantum operator which is represented as a matrix (two-dimensional numpy array).

        Parameter:
                matrix: One- or two-dimensional list or tuple -> Elements of the matrix, that represents the operator.
        """

        m = np.array(matrix)
        self._a = np.array(m, dtype=np.complex128).reshape(
            (int(np.sqrt(len(m.flatten()))), int(np.sqrt(len(m.flatten())))))
        self._num_qubits = int(np.log2(self._a.shape[0]))

        # Checks whether the provided matrix is unitary.
        if not np.allclose(self._a.dot(self._a.conj().T), np.eye(len(self._a))):
            raise ValueError(
                'Operators have to be unitary matrices. Please enter a valid operator.')

        # Checks whether each dimension of the matrix is a power of 2.
        if not np.log2(self._a.shape[0]).is_integer():
            raise ValueError(
                'Operators have to be matrices with 2**n rows/columns, where n is an integer (number of qubits).')

    def __repr__(self):
        s = str(self._a)
        return s

    def __str__(self):
        s = '{}-qubit operator. Operator matrix:\n'.format(self._num_qubits)
        s += str(self._a)
        return s

    def __getitem__(self, key):
        return self._a[key]

    def __add__(self, arg):
        return Operator(self._a + arg._a)

    def __sub__(self, arg):
        return Operator(self._a - arg._a)

    def __neg__(self):
        return Operator(-self._a)

    def __mul__(self, s):
        if isinstance(s, (float, int, complex)):
            return Operator(s * self._a)
        else:
                # It is only possible to multiply a operator with another operator.
            result = np.kron(self._a, s._a)
            result += 0.
            return Operator(result)

    def __rmul__(self, s):
        if isinstance(s, (float, int, complex)):
            return Operator(s * self._a)

    def __truediv__(self, s):
        return Operator(self._a / s)

    def __pow__(self, s):
        if isinstance(s, int):
            result = self._a
            for i in range(s - 1):
                result = np.kron(result, self._a)
            return Operator(result)
        else:
            raise ValueError(
                'It is only possible to use integers as the exponent for operators.')

    def __eq__(self, arg):
        if isinstance(arg, Operator):
            return np.array_equal(self._a, arg._a)
        else:
            return False

    def __call__(self, arg, qubit_ind=None):
        """
        With this function it is possible to apply the operator to another operator (operator composition) or to apply the operator to a state.
        Operator composition is only possible for two operators of the same size, in other words for two n-qubit operators.
        But it is possible to apply the n-qubit operator to a m-qubit state with n being smaller than m. If this is the case
        it is necessary to specify the qubits of the state to which the operator should be applied with the parameter qubit_ind.

        Parameters:
                arg: State or Operator -> The state the operator is applied to or the operator for operator composition.
                qubit_ind: Integer or iterable -> Index or indices of the qubits of the state that the operator is applied to (only usable if the operator is applied to a state).
        Return value: The resulting state of the operator application or the operator after the operator composition.
        Return type: State or Operator
        """
        from qcSim.state import State

        s_n = self._num_qubits
        a_n = arg._num_qubits

        if isinstance(arg, State):
            if s_n != a_n and qubit_ind is None:
                raise ValueError(
                    'This operator is designed for a {}-qubit state space.\n'
                    'The state you wanted to apply the operator to consists out of {} qubits.\n'
                    'Please provide a list with the indices of the state you want to apply the operator to.'.format(s_n, a_n))

            if qubit_ind is None:
                qubit_ind = range(a_n)
            qubit_ind = list(qubit_ind)
            not_applied_ind = sorted(
                list(set(range(a_n)) - set(qubit_ind)))

            if len(set(qubit_ind)) != len(qubit_ind):
                raise ValueError(
                    'The list of qubit indices contains repeated elements.')
            if min(qubit_ind) < 0:
                raise ValueError('Supplied qubit index < 0.')
            if max(qubit_ind) >= a_n:
                raise ValueError(
                    'Supplied qubit index is too large for this state.')
            if len(qubit_ind) != s_n:
                raise ValueError(
                    'Length of qubit_ind does not match operator.')

            # Rearranging the state so that the qubits to which the operator should be applied are at the beginning.
            state = arg._a.reshape([2] * arg._num_qubits)
            pre_trans = qubit_ind + not_applied_ind
            state = np.transpose(state, pre_trans).flatten()

            # Enlargement of the operator to the size of the state, by appending identity operators.
            identity = np.array([[1.0 + 0.0j, 0.0j], [0.0j, 1.0 + 0.0j]])
            operator = self._a
            for i in not_applied_ind:
                operator = np.kron(operator, identity)

            # Calculation of the resulting state and rearranging of the qubits into the initial order.
            result = operator.dot(state)
            result = result.reshape([2] * arg._num_qubits)
            back_trans = np.argsort(pre_trans)
            return_value = np.transpose(result, back_trans).flatten()

            return State(return_value)

        else:
            if s_n != a_n or qubit_ind is not None:
                raise ValueError(
                    'Only operators of the same size can be composed. \n'
                    'If you want to apply a smaller operator on certain qubits of a larger operator \n'
                    'use the identity operator and the operator multiplication to build an operator \n'
                    'of the corresponding size that only affects the desired qubits.')

            return Operator(self._a.dot(arg._a))

    def con_trans(self):
        """
        Get the conjugate transpose of this operator.

        Return value: The conjugate transpose operator.
        Return type: Operator
        """

        a = self._a.conj().T
        return Operator(a)


# Functions for creating specific quantum operators.


def identity(x=1):
    """
    Constructs the identity operator for x qubits.

    Parameter:
        x: Integer -> Number of qubits for that the operator is created, determines the size of the operator.
    Return value: A n×n matrix representing the operator.
    Return type: Operator
    """

    single_qubit_op = np.array([[1, 0], [0, 1]], dtype=np.complex128)
    result = 1

    for i in range(x):
        result = np.kron(result, single_qubit_op)

    return Operator(result)


def hadamard(x=1):
    """
    Constructs the Hadamard operator for x qubits.

    Parameter:
        x: Integer -> Number of qubits for that the operator is created, determines the size of the operator.
    Return value: A n×n matrix representing the operator.
    Return type: Operator
    """

    single_qubit_op = 1 / np.sqrt(2) * (
        np.array([[1, 1], [1, -1]], dtype=np.complex128))
    result = 1

    for i in range(x):
        result = np.kron(result, single_qubit_op)

    return Operator(result)


def pauli_x(x=1):
    """
    Constructs the Pauli X (bit flip) operator for x qubits.

    Parameter:
        x: Integer -> Number of qubits for that the operator is created, determines the size of the operator.
    Return value: A n×n matrix representing the operator.
    Return type: Operator
    """

    single_qubit_op = np.array([[0.0j, 1.0 + 0.0j], [1.0 + 0.0j, 0.0j]])
    result = 1

    for i in range(x):
        result = np.kron(result, single_qubit_op)

    return Operator(result)


def pauli_y(x=1):
    """
    Constructs the Pauli Y operator for x qubits.

    Parameter:
        x: Integer -> Number of qubits for that the operator is created, determines the size of the operator.
    Return value: A n×n matrix representing the operator.
    Return type: Operator
    """

    single_qubit_op = np.array([[0.0j, -1.0j], [1.0j, 0.0j]])
    result = 1

    for i in range(x):
        result = np.kron(result, single_qubit_op)

    return Operator(result)


def pauli_z(x=1):
    """
    Constructs the Pauli Z (phase flip) operator for x qubits.

    Parameter:
        x: Integer -> Number of qubits for that the operator is created, determines the size of the operator.
    Return value:
    Return type: Operator
    """

    single_qubit_op = np.array([[1.0 + 0.0j, 0.0j], [0.0j, -1.0 + 0.0j]])
    result = 1

    for i in range(x):
        result = np.kron(result, single_qubit_op)

    return Operator(result)


def rotation_x(theta):
    """
    Constructs the one qubit X-rotation operator, that rotates a state by an angel theta around the x-axis.

    Parameter:
        theta: float -> Rotation angle
    Return value: A n×n matrix representing the operator.
    Return type: Operator
    """

    return np.cos(theta / 2) * identity() - 1j * np.sin(theta / 2) * pauli_x()


def rotation_y(theta):
    """
    Constructs the one qubit Y-rotation operator, that rotates a state by an angel theta around the y-axis.

    Parameter:
        theta: float -> Rotation angle
    Return value: A n×n matrix representing the operator.
    Return type: Operator
    """

    return np.cos(theta / 2) * identity() - 1j * np.sin(theta / 2) * pauli_y()


def rotation_z(theta):
    """
    Constructs the one qubit Z-rotation operator, that rotates a state by an angel theta around the z-axis.

    Parameter:
        theta: float -> Rotation angle
    Return value: A n×n matrix representing the operator.
    Return type: Operator
    """

    return np.cos(theta / 2) * identity() - 1j * np.sin(theta / 2) * pauli_z()


def swap():
    """
    Constructs the Swap operator for a 2 qubit state.

    Return value: A 4×4 matrix representing the operator.
    Return type: Operator
    """

    return Operator(np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], dtype=np.complex128))


def cnot():
    """
    Constructs the 2-qubit CNOT-operator, which flips the second qubit (the target qubit) if and only if the first qubit (the control qubit) is set.

    Return value: A 4×4 matrix representing the operator.
    Return type: Operator
    """

    return Operator(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=np.complex128))


def toffoli():
    """
    Constructs the 3-qubit Toffoli-operator, which flips the third qubit if the first two qubits are both set.

    Return value: A 9×9 matrix representing the operator.
    Return type: Operator
    """

    result = np.eye(8)
    result[6:, 6:] = [[0, 1], [1, 0]]
    return Operator(result)


def controlled_operator(A):
    """
    Uses the x-quit operator A to construct a x+1-qubit controlled operator. This means only if the first qubit of the state is set (is in state |1>)
    the operator A is applied to the remaining qubits of the state.

    Parameter:
        A: Operator -> Operator for which the controlled operator should be produced.
    Return value: A n×n matrix representing the operator.
    Return type: Operator
    """

    x = int(np.log2(A._a.shape[0]))
    rows = 2**(x + 1)
    result = np.eye(rows, dtype=np.complex128)
    result[(2**x):, (2**x):] = A._a
    return Operator(result)


def u_f(x, f):
    """
    Constructs an x qubit u_f operator that marks the basis states for which the boolean function f returns 1 by changing the sign of their amplitudes.
    This operator is a central component of the Grover oracle and is also used in similar algorithms.

    Parameters:
        x: Integer -> Number of qubits for that the operator is created, determines the size of the operator.
        f: Function -> Boolean function, i.e. a function that only returns 0 or 1.
    Return value: A n×n matrix representing the operator.
    Return type: Operator
    """

    if x < 2:
        raise ValueError(
            'An u_f operator can only be constructed for a system with 2 or more qubits.')

    m = np.eye(2**x, dtype=np.complex128)

    # It is necessary to program the boolean function f in such a way that the function can handle a basis state as its parameter.
    for basis_state in itertools.product([0, 1], repeat=x):
        index = int("".join(str(i) for i in basis_state), 2)
        result = f(basis_state)

        if result not in [0, 1]:
            raise RuntimeError('Function f for u_f operator has to be a boolean function,'
                               'i.e., return 0 or 1.')

        if result:
            m[index, index] = -(1.0 + 0.0j)

    return Operator(m)


def two_pulse(theta, phi, global_phase=0.0):
    """
    Constructs a two-pulse single-qubit operator. This operator moves the qubit theta radians away from the positive z-axis, and phi radians away from the positive x-axis.
    By applying this operator with specific values for theta and phi to zero-initialized qubit the corresponding representation of the state in the Bloch sphere is created.

    Parameters:
        theta: float -> The angle of the state between the positive z-axis (|0⟩) and the negative z-axis (|1⟩) on the Bloch sphere.
        phi: float -> The angle between the positive x-axis and the projection of the state into the xy-plane on the Bloch sphere.
        global_phase : float -> The global phase applied to the state.
    Return value: A 2×2 matrix representing the operator.
    Return type: Operator
    """

    return Operator(np.array([[np.cos(theta / 2), -np.exp(1j * global_phase) * np.sin(theta / 2)], [np.exp(1j * phi) * np.sin(theta / 2), np.exp(1j * (phi + global_phase)) * np.cos(theta / 2)]], dtype=np.complex128))
