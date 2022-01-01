from anytree import NodeMixin, RenderTree
import uuid


class SyntaxTreeNode(NodeMixin):  
    def __init__(self, name, id, parent=None, children=None):
        self.name = name
        self.id = id
        self.parent = parent
        if children:
            self.children = children


def create_node(p):
    id = uuid.uuid4()
    children = []
    for i in range(len(list(p))):
        if i == 0:
            continue
        if type(p[i]).__name__ == SyntaxTreeNode.__name__:
            children.append(p[i])
        else:
            p[i] = create_node([p[i]])
            children.append(p[i])

    node = SyntaxTreeNode(p[0], id, children=children)
    return node
