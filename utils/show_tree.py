from anytree import RenderTree
from utils.color_prints import Colorprints

def show_tree(tree):
    Colorprints.print_in_lightPurple("Syntax Tree:")
    Colorprints.print_in_cyan(RenderTree(tree).by_attr('name'))
