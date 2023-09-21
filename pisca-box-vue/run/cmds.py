import __init__ # noqa: F401
import subprocess
import os
import libs.cmds as cmds

#DOCKER_SOURCE_DIR = "/project/xml"
DOCKER_SOURCE_DIR = "/mnt"
DOCKER_EXE = "/project/BEASTv1.8.4/bin/beast"


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
    #copy everything in tmp to pisca    
    try:        
        files=os.listdir(DOCKER_SOURCE_DIR)   
        for fname in files:            
            if ".xml" not in fname and (".log" in fname or ".ops" in fname or ".trees" in fname):
                os.rename(os.path.join(DOCKER_SOURCE_DIR,fname), os.path.join(DOCKER_SOURCE_DIR,"_" + fname))
    except Exception as e:
        print(str(e))
                
def run_beast(which_xml,params,TEST_MODE):    
    print("starting pisca-box call to beast...")    
    if not TEST_MODE:
        rename_logs()
    try:
        params.insert(0,"beast")                    
        docker = not TEST_MODE
        if docker:# DOCKER VERSION            
            params.append(DOCKER_SOURCE_DIR + "/" + which_xml)
        else: # LOCAL VERSION for testing            
            params.append(which_xml)
        return cmds.cmd_runner_with_wait(params)
    except Exception as e:
        print(str(e))
        return "failed"
            

