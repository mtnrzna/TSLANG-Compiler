from treelib import Node, Tree
import uuid


tree = Tree()
tree.create_node("Root", "root")

def add_childs(p):
    for i in range(1, len(p)):
        if hasattr(p[i], "identifier"):
            tree.move_node(p[i].identifier, p[0].identifier)
        else:
            p[i] = create_node(p[i])
            tree.move_node(p[i].identifier, p[0].identifier)



def create_node(node_tag):
    id = uuid.uuid4()
    return tree.create_node(node_tag, id , "root" )
