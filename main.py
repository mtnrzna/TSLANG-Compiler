from compile import Compiler

file_address = input("\033[97m{}\033[00m" .format("File Path: "))
file_not_found = False
try:
    with open(file_address) as f:
        data = f.read()
except:
    file_not_found = True

if not file_not_found:
    compiler = Compiler()
    compiler.compile(data, show_syntax_tree=True, print_error_messages=True)
else:
    print("Invalid File Path...")
