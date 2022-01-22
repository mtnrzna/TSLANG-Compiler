from compile import Compiler
from utils.color_prints import Colorprints
from utils.file import read_from_file

file_address = input("\033[97m {}\033[00m" .format("File Path: "))
#try:
data = read_from_file(file_address)
compiler = Compiler()
compiler.compile(data)
#except:
    #print("Invalid File Path...")
