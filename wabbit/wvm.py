# wvm.py


class WVM:
    def __init__(self):
        self.stack = []

    def PUSH(self, value):  # ALL CAPS = Machine instruction
        self.stack.append(value)

    def POP(self):
        return self.stack.pop()

    def ADD(self):
        right = self.POP()
        left = self.POP()
        self.PUSH(left + right)

    def SUB(self):
        right = self.POP()
        left = self.POP()
        self.PUSH(left - right)

    def MUL(self):
        right = self.POP()
        left = self.POP()
        self.PUSH(left * right)

    def IDIV(self):
        right = self.POP()
        left = self.POP()
        self.PUSH(left // right)

    def FDIV(self):
        right = self.POP()
        left = self.POP()
        self.PUSH(left / right)

    # useful instructions of whatever I want
    def PRINT(self):
        # not on a real CPU
        print(self.POP())
