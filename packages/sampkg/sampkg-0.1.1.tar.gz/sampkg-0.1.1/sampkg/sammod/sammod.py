import numpy as np


class Samclass(object):
    counter = 0

    def __init__(self, x="hello"):
        self.samstring = x
        type(self).counter += 1

    def __del__(self):
        type(self).counter -= 1

    def sam_inst_func(self):
        return "hello "+self.samstring


def sam_func(x):
    logval = np.log(Samclass.counter)
    return "{0:.2f} {1:s}".format(logval, x.samstring[::-1])
