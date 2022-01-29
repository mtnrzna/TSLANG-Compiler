class Colorprints(object):

    @staticmethod
    def print_in_red(str): print("\033[91m{}\033[00m".format(str))
    @staticmethod
    def print_in_green(str): print("\033[92m{}\033[00m".format(str))
    @staticmethod
    def print_in_yellow(str): print("\033[93m{}\033[00m".format(str))
    @staticmethod
    def print_in_lightPurple(str): print("\033[94m{}\033[00m".format(str))
    @staticmethod
    def print_in_purple(str): print("\033[95m{}\033[00m".format(str))
    @staticmethod
    def print_in_cyan(str): print("\033[96m{}\033[00m".format(str))
    @staticmethod
    def print_in_lightGray(str): print("\033[97m{}\033[00m".format(str))
    @staticmethod
    def print_in_black(str): print("\033[98m{}\033[00m".format(str))