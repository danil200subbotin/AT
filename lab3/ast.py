class Node(object):
    # object constructor
    def __init__(self, t='const', val=None,  ch=[], no=None, pos=None):
        self.type = t
        self.value = val
        self.child = ch
        self.lineno = no
        self.lexpos = pos

    def __repr__(self):
        return f'{self.type} {self.value}'

    def print(self, level=0):
        if self is None:
            return
        print(' - ' * level, self)
        if isinstance(self.child, list):
            for child in self.child:
                child.print(level + 1)
        elif isinstance(self.child, Node):
            self.child.print(level + 1)
        elif isinstance(self.child, dict):
            for key, value in self.child.items():
                print(' ' * (level + 1), key)
                if value:
                    value.print(level + 2)