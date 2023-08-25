import subprocess
import time
import os

DOCKER_SOURCE_DIR = "/project/xml"
DOCKER_EXE = "/project/BEASTv1.8.4/bin/beast"

def rename_logs(working_dir):
    #copy everything in tmp to pisca    
    try:        
        files=os.listdir(working_dir)   
        for fname in files:
            if not ".xml" in fname and (".log" in fname or ".ops" in fname or ".trees" in fname):
                os.rename(os.path.join(working_dir,fname), os.path.join(working_dir,"_" + fname))
    except Exception as e:
        print(str(e))
    
                
def run_beast(params):    
    print("starting pisca-box call to beast...")    
    #if not TEST_MODE:
    #rename_logs(working_dir)
    try:                        
        #docker = not TEST_MODE
        #if docker:# DOCKER VERSION
        #    params.insert(0,DOCKER_EXE)            
        #    result = subprocess.Popen(params,stdout=subprocess.PIPE,shell=False)                
        #else: # LOCAL VERSION for testing
        params.insert(0,"beast")                                             
        print(params)
        result = subprocess.Popen(params,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
        error_msg = False                  
        
        # Wait until process terminates
        while result.poll() is None:                    
            output = result.stdout.readline()            
            if not output :
                print("...waiting for beast to finish...")
            else:
                while output:
                    print(output.strip().decode('utf-8'))
                    output  = result.stdout.readline()                                                                                
            
            error = result.stderr.readline()
            while error:
                    if not error_msg:
                        print("##########################################")
                        print("Additional messages found:")
                        error_msg = True                                        
                    print("#",error.strip().decode('utf-8'))
                    error  = result.stderr.readline()                                                                                
            time.sleep(0.1)
        
        output  = result.stdout.readline()            
        if output :
            print(output.strip().decode('utf-8'))                                        
        rc = result.poll()             
        print("##########################################")
        print("...completed pisca-box")
        return ""
    except Exception as e:
        print(str(e))
    


    





