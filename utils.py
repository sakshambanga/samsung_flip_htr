
import numpy as np
import difflib

__author__ = "Daniel Vorberg"
__copyright__ = "Copyright (c) 2017, Daniel Vorberg"
__license__ = "GPL"


class Transformation:

    def __init__(self, param):
        if isinstance(param, np.ndarray):
            param = param.reshape(-1)
        self.matrix = np.stack([param[0:3], param[3:6], [0, 0, 1]])

    @classmethod
    def identity(cls):
        return cls([1, 0, 0, 0, 1, 0])

    @classmethod
    def translation(cls, x, y):
        return cls([1, 0, x, 0, 1, y])

    @classmethod
    def rotation(cls, angle):
        return cls([np.cos(angle), - np.sin(angle), 0,
                    np.sin(angle),   np.cos(angle), 0])

    @classmethod
    def scale(cls, factor):
        if isinstance(factor, tuple):
            return cls([factor[0], 0, 0, 0, factor[1], 0])
        else:
            return cls([factor, 0, 0, 0, factor, 0])

    @classmethod
    def shear(cls, x_angle=0, y_angle=0):
        return cls([1, np.tan(y_angle), 0, np.tan(x_angle), 1, 0])

    @classmethod
    def mirror(cls, angle):
        return cls([np.cos(angle),  np.sin(angle), 0,
                    np.sin(angle), -np.cos(angle), 0])

    @property
    def parameter(self):
        return self.matrix.reshape(-1)[[0, 3, 1, 4, 2, 5]]

    @property
    def determinant(self):
        return np.linalg.det(self.matrix)

    def __matmul__(self, other):
        if isinstance(other, np.ndarray):
            return other @ self.matrix[:2, :2].transpose() + self.matrix[:2, 2]
        elif isinstance(other, Transformation):
            return Transformation(self.matrix @ other.matrix)
        else:
            return NotImplemented

    def __invert__(self):
        return Transformation(np.linalg.inv(self.matrix))


def colored_str_comparison(text, n_text):
    """ Unify operations between two compared strings seqm is a difflib.
        SequenceMatcher instance whose a & b are strings
        cnf. http://stackoverflow.com/a/788780
    """
    seqm = difflib.SequenceMatcher(None, text, n_text)
    output= ""
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLACK = '\033[0m'
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            output += seqm.a[a0:a1]
        elif opcode == 'insert':
            output += RED + seqm.b[b0:b1] + BLACK
        elif opcode == 'delete':
            output += GREEN + seqm.a[a0:a1] + BLACK
        elif opcode == 'replace':
            output += GREEN + seqm.a[a0:a1] + RED + seqm.b[b0:b1] + BLACK
        else:
            raise RuntimeError
    return ''.join(output)


def cached_property(function):
    """ decorator to strore the results of a method
    """
    attr_name = '_cached_' + function.__name__

    @property
    def _chached_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, function(self))
        return getattr(self, attr_name)
    return _chached_property
