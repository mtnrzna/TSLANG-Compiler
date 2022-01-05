from anytree import RenderTree

def show_tree(tree):
    print("Syntax Tree:")
    print(RenderTree(tree).by_attr('name'))
