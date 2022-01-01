from anytree import RenderTree

def show_tree(tree):
    print(RenderTree(tree).by_attr('name'))
