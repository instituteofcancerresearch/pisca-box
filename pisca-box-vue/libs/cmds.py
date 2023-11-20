import subprocess
import time
import os

#DOCKER_SOURCE_DIR = "/project/xml"
#DOCKER_EXE = "/project/BEASTv1.8.4/bin/beast"
VERSION = "0.0.2"

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


def run_r_script(treefl,logfl,age,outputfl,title):
    #mccTreeFile=args[1]
    #logDataFile=args[2]
    #outputfile=args[3]
    #title=args[4]
    #age=as.numeric(args[5])
    print("Welcome to pisca-box version " + VERSION)    
    script = "app/scripts/pisca-plot.R"
    cmd_runner_with_wait(["chmod","+x",script])
    params = ["Rscript",script,treefl,logfl,outputfl,title,str(age)]
    return cmd_runner_with_wait(params)
    

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
            if ".xml" not in fname and (".log" in fname or ".ops" in fname or ".trees" in fname):
                os.rename(os.path.join(working_dir,fname), os.path.join(working_dir,"_" + fname))
    except Exception as e:
        print(str(e))
                            
def run_beast(params):
    print("Welcome to pisca-box version " + VERSION)
    print("starting pisca-box call to beast...")
    try:
        params.insert(0,"beast")
        print(params)
        return cmd_runner_with_wait(params)
    except Exception as e:
        print(str(e))
        return "failed"
    

def run_tree_from_file(tree_file, burnin,output_file):
    print("Welcome to pisca-box version " + VERSION)
    print("starting pisca-box call to treeannotator...")
    try:
        #treeannotator -burnin 5000000 pisca.run.trees output.mcc.tree        
        with open(output_file, "w") as text_file:
            text_file.write("")
        params = ["treeannotator","-burnin",str(burnin), tree_file,output_file]
        print(params)
        return cmd_runner_with_wait(params)
    except Exception as e:
        print(str(e))
        return "failed"
    
def run_tree(tree_str, burnin,output_file):
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
        return cmd_runner_with_wait(params)
    except Exception as e:
        print(str(e))
        return "failed"
    

    





