import numpy as np
import itertools


class State():
    """
    Instances of the state class represent quantum states. These quantum states can be single or multi-qubit systems.
    This class also contains some functions for creating specific quantum states.
    """

    def __init__(self, vector):
        """
        Creates a quantum state which is represented as a column vector (one-dimensional numpy array) with the provided amplitudes.

        Parameter:
            vector: List or tuple -> Amplitudes of the state that should be created.
        """

        # Checks whether the provided vector has 2**n elements (n is the number of qubits).
        array = np.array(vector)
        if not np.log2(array.size).is_integer():
            raise ValueError(
                'State vector does not have (2**n) components. Please enter a valid number of amplitudes.')

        self._a = np.array(vector, dtype=np.complex128)
        self._num_qubits = int(np.log2(self._a.size))

        if np.sum(np.square(self._a)) == 0:
            raise ValueError(
                'Please provide reasonable amplitudes. It is not possible that all amplitudes are 0.')

        # Normalization of the amplitudes, if they are not already normalized.
        if not self.is_normalized():
            self.renormalize()

    def is_normalized(self):
        """
        Checks if a state is normalized.

        Return value: True if the state is normalized and False if the state is not normalized.
        Return type: Boolean
        """

        x = np.real(self.dot(self)) - 1
        if -0.01 <= x <= 0.01:
            return True
        else:
            return False

    def renormalize(self):
        """
        Normalizes a state, so that the sum of the squares of all amplitudes is 1.
        """

        n_factor = np.sqrt(np.real(self.dot(self)))
        self._a = self._a / n_factor

    def dot(self, state2):
        """
        Calculates the dot product between two states.

        Parameter:
            state2: State -> The second State for calculating the dot product.
        Return value: The dot product with state2
        Return type: Complex number
        """

        return np.sum(np.conj(self._a) * state2._a)

    def inner(self, state2):
        """
        Calculates the inner product between two states.

        Parameter:
            state2: State -> The second State for calculating the inner product.
        Return value: The inner product with state2.
        Return type: Complex number
        """

        return np.inner(self._a, state2._a)

    def probabilities(self):
        """
        Calculates the probabilities with which each basis state is observed during a measurement.

        Return value: The probability associated with each basis state.
        Return type: One-dimensional numpy array of type float
        """

        probs = np.real(np.conj(self._a) * self._a)
        return probs

    def specific_probability(self, *bits):
        """
        Calculates the probability of observing a specific basis state during a measurement. It is also possible to determine
        the probability of measuring one or more qubits of a multi-qubit system in a specific state.
        If a specific qubit should be exclude, use 'None' as the argument at the position of this qubit.
        For example: State A is a 3-qubit state. By calling A.specific_probability(1,None,0) the probability P of measuring
        qubit1 of system A in state |1> and qubit3 of system A in state |0> is calculated (P = p(|100>) + p(|110>)).

        Parameter:
            *bits: Variable number of arguments with the value of 0, 1 or None.
                    -> Encodes the basis state for which the probability should be calculated.
        Return value: The specific probability of measuring the provided basis state.
        Return type: Float
        """

        n = self._num_qubits
        tensor_representation = self._a.reshape([2] * n)

        if len(bits) > n:
            raise ValueError(
                'The number of qubits of the provided basis state is to high.')

        if len(bits) < n:
            raise ValueError(
                "The number of qubits of the provided basis state is to low.\n"
                "Use 'None' if you want to exclude certain qubits.\n"
                "For example: If you have a 4-qubit state and you only want to know the probability \n"
                "of measuring a 0 for the first qubit provide '0, None, None, None'.")

        for i in bits:
            if not (i == 1 or i == 0 or i is None):
                raise ValueError(
                    "The provided arguments do not represent a basis state.\n"
                    "Please note that the arguments should have the value of 0 or 1.\n"
                    "For example: By providing '1, 1, 1' the probability of the bassis state |111> is calculated.")

        possible_combinations = list(
            itertools.product([0, 1], repeat=self._num_qubits))

        for index in range(len(bits)):
            if bits[index] is not None:
                possible_combinations = [
                    combination for combination in possible_combinations if combination[index] == bits[index]]

        result = 0

        for combination in possible_combinations:
            result += np.real(
                np.conj(tensor_representation[combination]) * tensor_representation[combination])

        return result

    def measure(self, qubit_ind=None, remove=False):
        """
        Measures the current state. If a list of qubit indices is given only these qubits are measured. If no list is given, every qubit is measured.
        By measuring a qubit its superposition is destroy (the state collapses) and and the result of the measurement is that the qubit is either in state |0> or in state |1>.

        Parameters:
            qubit_ind: Integer or iterable -> Index or indices of the qubits that should be measured.
            remove: Boolean -> Defines whether the measured qubits should be removed from the state.
        Return value: The results for the measured qubits.
        Return type: Integer or tuple of integers
        """

        if qubit_ind is None:
            qubit_ind = range(self._num_qubits)

        tensor_representation = self._a.reshape([2] * self._num_qubits)

        qubit_ind_int = False
        if isinstance(qubit_ind, int):
            qubit_ind = [qubit_ind]
            qubit_ind_int = True

        qubit_ind = list(qubit_ind)

        if qubit_ind == []:
            raise ValueError(
                'You have to define at least one qubit that should be measured.')

        if min(qubit_ind) < 0 or max(qubit_ind) >= self._num_qubits:
            raise ValueError(
                'Trying to measure a qubit index that does not exist.\n'
                'Remember: Qubit-indices go from 0 to (d-1), where d is the total number of qubits in the current state.')

        # Computation of the probability of each possible outcome for the measured qubits.
        num_poss_measurement = 2**len(qubit_ind)
        unmeasured_ind = list(set(range(self._num_qubits)) - set(qubit_ind))
        permutation = qubit_ind + unmeasured_ind
        rearranged_amplitudes = np.transpose(
            tensor_representation, permutation)
        probabilities = np.reshape(np.real(
            rearranged_amplitudes * np.conj(rearranged_amplitudes)), (num_poss_measurement, -1)).sum(axis=1)

        # Generates the random result of the measurement - each result occurs with its associated probability.
        result = np.random.choice(num_poss_measurement, p=probabilities)

        # Creates binary representation of measured state
        bits = self._binary(result, len(qubit_ind))

        # Amplitudes of the remaining qubits after measurement (Explanation: Hoemeister S. 47).
        x = probabilities[result]
        new_amplitudes = rearranged_amplitudes[bits] / np.sqrt(x)

        # State after measurement depending on whether the measured qubits should be removed or not.
        if remove:
            self._a = new_amplitudes.flatten()
            self._num_qubits = int(np.log2(self._a.size))
        else:
            rearranged_amplitudes = np.zeros_like(rearranged_amplitudes)
            rearranged_amplitudes[bits] = new_amplitudes
            self._a = np.transpose(rearranged_amplitudes,
                                   np.argsort(permutation)).flatten()

        if qubit_ind_int:
            bits = bits[0]

        self.renormalize()

        return bits

    def dirac_basis(self):
        """
        Generates the Dirac notation for a basis state. Therefore each qubit of the state object which this function is applied to has to be in state |0> or |1>.

        Return value: The Dirac notation
        Return type: Tuple of integers
        """

        for i in self._a.real:
            if not (i == 1 or i == 0):
                raise ValueError(
                    'This function only produces the Dirac-Notation for basis states. The state provided is no basis state.')

        possible_combinations = list(
            itertools.product([0, 1], repeat=self._num_qubits))

        for index, value in enumerate(self._a):
            if value.real == 1:
                return possible_combinations[index]

    def probs_with_state(self, remove=True):
        """
        Assigns to each possible basis state the probability with which it can be observed during a measurement.
                The functionality is very similar to method probabilities(), but this method also explicitly names the individual basis states.

        Parameter:
            remove: Boolean -> If True all basis states with a probability of 0 are not included in the return value.
        Return value: A collection of the possible observations after measurement with their associated probabilities.
        Return type: Dictionary of tuples (basis states) and floats (probabilities)
        """

        probs = np.real(np.conj(self._a) * self._a)

        if remove:
            dirac = [0] * np.count_nonzero(probs)
            counter = 0

            for index, value in enumerate(probs):
                if value != 0:
                    dirac[counter] = self._binary(index, self._num_qubits)
                    counter += 1

            probs = probs[probs != 0]

        else:
            dirac = [0] * len(probs)

            for index, value in enumerate(probs):
                dirac[index] = self._binary(index, self._num_qubits)

        return dict(zip(dirac, probs))

    def __repr__(self):
        s = str(self._a)
        return s

    def __str__(self):
        s = '{}-qubit state. State vector:\n'.format(int(self._num_qubits))
        s += str(self._a)
        return s

    def __getitem__(self, key):
        return self._a[key]

    def __add__(self, arg):
        return State(self._a + arg._a)

    def __sub__(self, arg):
        return State(self._a - arg._a)

    def __neg__(self):
        return State(-self._a)

    def __mul__(self, s):
        if isinstance(s, (float, int, complex)):
            return State(s * self._a)
        else:
            # It is only possible to multiply a state with another state.
            return State(self.tensor_product(s))

    def __rmul__(self, s):
        if isinstance(s, (float, int, complex)):
            return State(s * self._a)

    def __truediv__(self, s):
        return State(self._a / s)

    def __pow__(self, s):
        if isinstance(s, int):
            x = State(self._a)
            for i in range(s - 1):
                x = State(x.tensor_product(self))
            return x
        else:
            raise ValueError(
                'It is only possible to use integers as the exponent for states.')

    def __eq__(self, arg):
        if isinstance(arg, State):
            return np.array_equal(self._a, arg._a)
        else:
            return False

    def tensor_product(self, arg):
        """
        Calculates the tensor product of two state vectors.

        Parameter:
            arg: State -> Second state for calculating the tensor product.
        Return value: The resulting vector of the calculation.
        Return type: One-dimensional numpy array
        """

        tensor1 = self._a.reshape([2] * self._num_qubits)
        tensor2 = arg._a.reshape([2] * arg._num_qubits)
        return np.tensordot(tensor1, tensor2, axes=0).flatten()

    @staticmethod
    def _binary(x, l):
        """
        Generates the binary representation of a certain length L as a tuple for a specific number X.

        Parameters:
            x: Integer -> The number for which the binary representation should be generated.
            l: Integer -> Length of the binary representation.
        Return value: Binary representation of the number.
        Return type: Tuple of zeros and ones
        """

        binary = list(map(int, bin(x)[bin(x).find('b') + 1:]))
        if len(binary) < l:
            binary = [0] * (l - len(binary)) + binary
        return tuple(binary)


# Functions for creating specific quantum states.
from qcSim.operators import hadamard, cnot, identity


def qubit(*, alpha=None, beta=None, theta=None, phi=None, global_phase=0.0):
    """
    Generates a specific single qubit state.

    Parameters:
        alpha: Float -> Probability amplitude for the state |0⟩.
        beta: Float -> Probability amplitude for the state |1⟩.
        theta: Float -> The angle of the state between the positive z-axis (|0⟩) and the negative z-axis (|1⟩) on the Bloch sphere.
        phi: Float -> The angle between the positive x-axis and the projection of the state into the xy-plane on the Bloch sphere.
        global_phase : Float -> The global phase applied to the state.
    Return value: The state that was specified either by alpha and beta or by theta, phi and global_phase.
    Return type: State
    """

    # Either alpha and beta or theta and phi should be given. Not both!
    if alpha is not None and beta is not None and theta is None and phi is None:
        vector = np.zeros(2, dtype=np.complex128)
        vector[0] = alpha
        vector[1] = beta
    elif alpha is None and beta is None and theta is not None and phi is not None:
        vector = np.zeros(2, dtype=np.complex128)
        alpha = np.cos(theta / 2)
        beta = np.sin(theta / 2) * np.exp(1j * phi)
        vector[0] = alpha
        vector[1] = beta
    else:
        raise ValueError(
            'Please provide a correct combination of arguments for the qubit. Provide alpha and beta or theta and phi.')

    state = State(vector * np.exp(1j * global_phase))
    return state


def zeros(n=1):
    """
    Generates the basis vector for a state with n qubits, which all have a value of |0> (the all-zero basis vector).

    Parameter:
        n: Integer -> Number of qubits for the state.
    Return value: A n-qubit state with all qubits in the state |0>.
    Return type: State
    """

    if n < 1:
        raise ValueError(
            'Please provide a valid number of qubits (at least 1).')

    num_elements = 2**n
    v = np.zeros(num_elements, dtype=np.complex128)
    v[0] = 1

    return State(v)


def ones(n=1):
    """
    Generates the basis vector for a state with n qubits, which all have a value of |1> (the all-one basis vector).

    Parameter:
        n: Integer -> Number of qubits for the state.
    Return type: A n-qubit state with all qubits in the state |1>.
    Return value: State
    """

    if n < 1:
        raise ValueError(
            'Please provide a valid number of qubits (at least 1).')

    num_elements = 2**n
    v = np.zeros(num_elements, dtype=np.complex128)
    v[-1] = 1

    return State(v)


def bit_array(*bits):
    """
    Generates the basis state for a given bit sequence. That means each qubit of the generated state has the either the value of |0> or of |1>.

    Parameters:
        *bits: Variable number of arguments with the value of 0 or 1 -> Bit representation of the n-qubit state.
    Return type: A state describing the provided bit sequence.
    Return value: State
    """

    n = len(bits)

    if n == 0:
        raise ValueError('Provide at least the value of one qubit.')

    for i in bits:
        if not (i == 1 or i == 0):
            raise ValueError(
                'The parameters of the bit_array function should be 0 or 1.')

    possible_combinations = list(itertools.product([0, 1], repeat=n))

    v = np.zeros((2 ** n))

    for index, value in enumerate(possible_combinations):
        if value == bits:
            v[index] = 1

    return State(v)


def bell_state(qubit1=0, qubit2=0):
    """
    Generates one of the four 2-qubit Bell states.

    Parameters:
        qubit1: {0, 1} -> Value of the first qubit before entanglement.
        qubit2: {0, 1} -> Value of the second qubit before entanglement.
    Return value: A 2-qubit Bell state.
    Return type: State
    """

    if qubit1 not in [0, 1] or qubit2 not in [0, 1]:
        raise ValueError(
            'The provided values for creating a Bell state have to be 0 or 1.')

    a = bit_array(qubit1, qubit2)
    X = cnot()(hadamard() * identity())

    return X(a)
