import subprocess

# This part uses compiled file of TSLVM by  "Ali Gholami Rudi"
# TSVM: TSLANG INTERMEDIATE REPRESENTATION VIRTUAL MACHINE
# link: https://github.com/aligrudi/tsvm

class RunTSVM(object):

    def run(self):        
        #subprocess.run(["gcc", "-w", "-o", ".\compiler_levels\IR_generation\\tsvm\\a.exe", ".\compiler_levels\IR_generation\\tsvm\\tsvm.c"])
        subprocess.run([".\compiler_levels\IR_generation\\tsvm.exe", ".\compiler_levels\IR_generation\generated_IR.txt"])
        # character "\" before characters "t" and "a" should be escaped! 
        
