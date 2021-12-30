# File
def read_from_file(file_address):
    file = open(file_address, "r")
    data = file.read()
    return data
