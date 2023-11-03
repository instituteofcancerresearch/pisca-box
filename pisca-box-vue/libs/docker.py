import subprocess
import time
import os

VERSION = "0.0.3"

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
                                
def beast_docker(full_file_name,docker_params,docker_version):
    #docker run -v ~/dev/beast-icr/pisca-branch:/mnt --rm pisca-branch-master flipflop.xml
    dir = os.getcwd()    
    params = ["docker", "run", "--privileged","-v", f"{dir}:/mnt", "--rm", docker_version, full_file_name] + docker_params
    print("Welcome to pisca-box version " + VERSION)
    print("starting pisca-box call to beast...")        
    try:                                        
        print(params)
        return cmd_runner_with_wait(params)                
    except Exception as e:
        print(str(e))
        return "failed"
    


