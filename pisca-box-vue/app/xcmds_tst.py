import subprocess
import time
import os

DOCKER_SOURCE_DIR = "/project/xml"
DOCKER_EXE = "/project/BEASTv1.8.4/bin/beast"

def rename_logs():
    print("renaming log files")    
    
                
def run_beast(params):    
    print("starting pisca-box call to beast...")    
    #if not TEST_MODE:
    #    rename_logs()    
    loops = 10        
    i = 0
    # Wait until process terminates
    while i < loops:
        output  = f"Loops{i}"        
        print(output)        
        time.sleep(0.1)        
        i += 1
    print("...finished")                                            
    return ""



