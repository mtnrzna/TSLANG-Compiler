import os
import config
from compile import Compiler
from utils.color_prints import Colorprints

file_address = input("\033[97m{}\033[00m" .format("File Path: "))
file_not_found = False
try:
    with open(file_address) as f:
        data = f.read()
        config.code_file_path = os.path.abspath(file_address)
except:
    file_not_found = True

if not file_not_found:
    compiler = Compiler()
    compiler.compile(data, show_syntax_tree=True, print_error_messages=True)
else:
    Colorprints.print_in_red("Invalid File Path...")
