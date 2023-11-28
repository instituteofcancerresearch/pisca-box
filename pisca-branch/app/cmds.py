import subprocess
import time
import os

VERSION = "0.0.2"
DOCKER_SOURCE_DIR = "/mnt"
DOCKER_EXE = "beast"

def cmd_runner_with_wait(params):
    print("...opening process...")
    result = subprocess.Popen(params,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False)
    error_msg = False
    any_exceptions = False
    # Wait until process terminates
    while result.poll() is None:                    
        print("...waiting for process to finish...")
        output = result.stdout.readline()            
        if output:                                
            while output:
                if "SEVERE" in output.strip().decode('utf-8'):
                    any_exceptions = True
                if "ERROR" in output.strip().decode('utf-8'):
                    any_exceptions = True
                print(output.strip().decode('utf-8'))
                output  = result.stdout.readline()                                                                                        
        error = result.stderr.readline()
        while error:
            if not error_msg:
                print("##########################################")
                print("Additional messages found:")
                error_msg = True                                        
            print("#",error.strip().decode('utf-8'))
            if "SEVERE" in error.strip().decode('utf-8'):
                any_exceptions = True
            if "ERROR" in error.strip().decode('utf-8'):
                any_exceptions = True
            error  = result.stderr.readline()                                                                                
        time.sleep(0.1)    
    output  = result.stdout.readline()            
    if output:
        print(output.strip().decode('utf-8'))                                        
    result.poll()
    print("##########################################")    
    if any_exceptions:
        print("!!! failed pisca-box")
        return "failed" 
    else:
        print("...completed pisca-box")
        return "done"

    
def run_validation(dirs):
    """Run validation command."""    
    print("listing files...")
    result01 = subprocess.run(["ls","-l"],stdout=subprocess.PIPE)    
    result02 = ""
    for dir in dirs:
        result = subprocess.run(["ls",dir,"-l"],stdout=subprocess.PIPE)
        result02 = result.stdout.decode('utf-8') + "\n"
    result03 = subprocess.run(["java","-version"],stdout=subprocess.PIPE)
    
    return result01.stdout.decode('utf-8') + "\n" + result02 + "\n" + result03.stdout.decode('utf-8')

def rename_logs():    
    try:        
        files=os.listdir(DOCKER_SOURCE_DIR)   
        for fname in files:            
            if ".xml" not in fname and (".log" in fname or ".ops" in fname or ".trees" in fname):
                print("...",fname) 
                os.rename(os.path.join(DOCKER_SOURCE_DIR,fname), os.path.join(DOCKER_SOURCE_DIR,"_" + fname))
    except Exception as e:
        print(str(e))

                
def run_beast(which_xml,params):    
    print("starting pisca-box call to beast...")        
    try:
        # check xml file
        full_xml = which_xml 
        if not os.path.isfile(full_xml): #if we run from python
            full_xml = DOCKER_SOURCE_DIR + "/" + which_xml # if we have mounted in a container   
        params.insert(0,DOCKER_EXE)                                            
        params.append(full_xml)
        return cmd_runner_with_wait(params)
    except Exception as e:
        print(str(e))
        return "failed"
    
    