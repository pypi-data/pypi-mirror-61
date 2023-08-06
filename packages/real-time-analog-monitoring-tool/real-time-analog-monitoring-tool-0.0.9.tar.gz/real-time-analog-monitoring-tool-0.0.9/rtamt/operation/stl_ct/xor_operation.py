from rtamt.operation.abstract_operation import AbstractOperation
import rtamt.operation.stl_ct.intersection as intersect

class XorOperation(AbstractOperation):
    def __init__(self):
        self.left = []
        self.right = []

    def update(self, *args, **kargs):
        out = []
        left_list = args[0]
        right_list = args[1]
        self.left = self.left + left_list
        self.right = self.right + right_list

        out = intersect.intersection(self.left, self.right, intersect.xor)

        return out
