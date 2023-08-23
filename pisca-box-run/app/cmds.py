import subprocess
import time
import shutil
import os

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
    #copy everythong in tmp to pisca    
    src_dir = '/project/xml'    
    files=os.listdir(src_dir)   
    for fname in files:
        if not ".xml" in fname:            
            os.rename(os.path.join(src_dir,fname), os.path.join(src_dir,"_" + fname))
        
def run_beast01(which_xml,is_docker):
    """Run beast01 command."""    
    print("starting beast...")    
    try:
        if which_xml == "":
            which_xml1 = "/project/BEASTv1.8.4/examples/testXML/testLikelihood.xml"
        else:
            which_xml1 = "/project/xml/" + which_xml            
        if not is_docker:
            which_xml1 = "/home/ralcraft/dev/beast-icr/xml/testStrictClock.xml"
                                                                
        if is_docker:
            result = subprocess.Popen(["/project/BEASTv1.8.4/bin/beast","-beagle_off", "-working", "-overwrite", which_xml1],stdout=subprocess.PIPE,shell=False)
        else:
            result = subprocess.Popen(["beast","-beagle_off", "-overwrite", which_xml],stdout=subprocess.PIPE,shell=False)
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
        return ""
    except Exception as e:
        return str(e)
    

def run_pisca01(which_xml):
    """Run beast01 command."""    
    print("starting beast...")
    try:
        if which_xml == "":
            which_xml = "/project/PISCAv1.1/validation.xml"
        else:
            which_xml = "/project/xml/" + which_xml
            
        result = subprocess.run(["/project/BEASTv1.8.4/bin/beast","-beagle_off", "-working", "-overwrite", which_xml],stdout=subprocess.PIPE)
        print(result)
        return result.stdout.decode('utf-8')
    except Exception as e:
        return str(e)
    
    