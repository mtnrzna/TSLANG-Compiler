from utils.color_prints import Colorprints

class SemanticErrors(object):
    errors = 0
    error_messages = []
    @staticmethod
    def print_error_messages():
        SemanticErrors.error_messages.sort(key=SemanticErrors.sort_by_lineno)
        for er_msg in SemanticErrors.error_messages:
            Colorprints.print_in_red(er_msg["message"])
    @staticmethod
    def add_error(error):
        if not error in SemanticErrors.error_messages:
            SemanticErrors.error_messages.append(error)
            SemanticErrors.errors += 1 


    @staticmethod
    def sort_by_lineno(er_msg):
        return er_msg["lineno"]
