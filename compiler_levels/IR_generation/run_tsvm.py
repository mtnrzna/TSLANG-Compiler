import subprocess
from utils.color_prints import Colorprints

# This part uses compiled file of TSLVM by  "Ali Gholami Rudi"
# TSVM: TSLANG INTERMEDIATE REPRESENTATION VIRTUAL MACHINE
# link: https://github.com/aligrudi/tsvm

class RunTSVM(object):

    def run(self):        
        #subprocess.run(["gcc", "-w", "-o", ".\compiler_levels\IR_generation\\tsvm\\tsvm.exe", ".\compiler_levels\IR_generation\\tsvm\\tsvm.c"])
        return_code = subprocess.run([".\compiler_levels\IR_generation\\tsvm.exe", ".\compiler_levels\IR_generation\generated_IR.txt"]).returncode
        if return_code == 0:
            Colorprints.print_in_purple(f"execution ended with return code: {return_code}")
        else:
            Colorprints.print_in_red(f"execution ended with return code: {return_code}")            
        # character "\" before characters "t" and "a" should be escaped! 
        
