class Node(object):
    # object constructor
    def __init__(self, type_='const', value_=None, child_=None, line_number_=None, position_=None):
        if child_ is None:
            child_ = []
        self.type = type_
        self.value = value_
        self.child = child_
        self.lineno = line_number_
        self.lexpos = position_

    def print(self, level=0):
        if self is None:
            print("-----------------WHAT?----------------")
            return
        print(' | ' * level, self)
        if isinstance(self.child, list):
            for child in self.child:
                child.print(level + 1)
        elif isinstance(self.child, Node):
            self.child.print(level + 1)
        else:
            print("[my_ast.py] cnfui gvyoufbhwkbhv bfhuwbhvkfhwbvh bcuosv byufobuv bf ui)")

    def __repr__(self):
        return f'{self.type} {self.value}'


