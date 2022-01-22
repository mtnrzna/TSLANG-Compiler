from compile import Compiler
from utils.file import read_from_file

file_address = input("File Path: ")
#try:
data = read_from_file(file_address)
compiler = Compiler()
compiler.compile(data)
#except:
    #print("Invalid File Path...")
