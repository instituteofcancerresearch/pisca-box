import subprocess
import time
import os

DOCKER_SOURCE_DIR = "/project/xml"
DOCKER_EXE = "/project/BEASTv1.8.4/bin/beast"

def rename_logs():
    print("") # not sure I need to do this as it is docker only
    
                
def run_beast(params,TEST_MODE):    
    print("starting pisca-box call to beast...")    
    if not TEST_MODE:
        rename_logs()
    try:                        
        docker = not TEST_MODE
        if docker:# DOCKER VERSION
            params.insert(0,DOCKER_EXE)            
            result = subprocess.Popen(params,stdout=subprocess.PIPE,shell=False)                
        else: # LOCAL VERSION for testing
            params.insert(0,"beast")                                             
            print(params)
            result = subprocess.Popen(params,stdout=subprocess.PIPE,shell=False)                        
        
        # Wait until process terminates
        while result.poll() is None:                    
            output  = result.stdout.readline()            
            if not output :
                print("...waiting for beast to finish...")
            else:
                while output:
                    print(output .strip().decode('utf-8'))
                    output  = result.stdout.readline()                        
            time.sleep(0.1)
        
        output  = result.stdout.readline()            
        if output :
            print(output.strip().decode('utf-8'))                                        
        rc = result.poll()        
        print("...completed pisca-box")
        return ""
    except Exception as e:
        print(str(e))
    





