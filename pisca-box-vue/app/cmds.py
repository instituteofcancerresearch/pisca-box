import subprocess
import time
import os

#DOCKER_SOURCE_DIR = "/project/xml"
#DOCKER_EXE = "/project/BEASTv1.8.4/bin/beast"
VERSION = "0.0.2"

def run_validation(dirs):
    """Run validation command."""    
    print("listing files...")
    result01 = "Current: " + subprocess.run(["ls","-l"],stdout=subprocess.PIPE).stdout.decode('utf-8')
    #result02 = ""
    #for dir in dirs:
    #    result = subprocess.run(["ls",dir,"-l"],stdout=subprocess.PIPE)
    #    result02 = dir + ":" + result.stdout.decode('utf-8') + "\n"
    #result03 = "java:" + subprocess.run(["java","-version"],stdout=subprocess.PIPE).stdout.decode('utf-8')
    result04 = "pwd:" + subprocess.run(["pwd"],stdout=subprocess.PIPE).stdout.decode('utf-8')
    
    #return f"{result01}\n{result02}\n{result03}\n{result04}"
    return f"{result01}\n{result04}"

def get_logs(big_string,log_match):
    ls_big_string = big_string.split("\n")
    for line in ls_big_string:
        if log_match in line:
            ls_line = line.split(" ")
            for item in ls_line:
                if log_match in item:
                    eq_line = item.split("=")
                    log_file = eq_line[1][1:-1]
                    log_file = log_file.replace("<","")
                    log_file = log_file.replace(">","")
                    log_file = log_file.replace('"',"")
                    log_file = log_file.replace("'","")
                    return log_file
    return ""
                                
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
    print("Welcome to pisca-box version " + VERSION)
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
        return "done"
    except Exception as e:
        print(str(e))
        return "failed"
    

def run_tree(log_str, tree_str, burnin,output_file):
    print("Welcome to pisca-box version " + VERSION)
    print("starting pisca-box call to treeannotator...")        
    try:                                
        #treeannotator -burnin 5000000 pisca.run.trees output.mcc.tree
        with open("pisca.run.trees", "w") as text_file:
            text_file.write(tree_str)
            
        with open(output_file, "w") as text_file:
            text_file.write("")
            
        params = ["treeannotator","-burnin",str(burnin), "pisca.run.trees",output_file]        
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
        return "done"
    except Exception as e:
        print(str(e))
        return "failed"
    

    





