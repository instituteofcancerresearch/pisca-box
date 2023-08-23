import subprocess
import time

def run_validation(dir):
    """Run validation command."""    
    print("listing files...")
    #result01 = subprocess.run(["ls","-l"],stdout=subprocess.PIPE)
    result01 = subprocess.run(["pwd"],stdout=subprocess.PIPE)    
    result02 = subprocess.run(["ls",dir,"-l"],stdout=subprocess.PIPE)
    result03 = subprocess.run(["java","-version"],stdout=subprocess.PIPE)
    
    return result01.stdout.decode('utf-8') + "\n" + result02.stdout.decode('utf-8') + "\n" + result03.stdout.decode('utf-8')



def run_beast01(which_xml,is_docker):
    """Run beast01 command."""    
    print("starting beast...")
    try:
        if which_xml == "":
            which_xml = "/project/BEASTv1.8.4/examples/testXML/testLikelihood.xml"
        else:
            which_xml = "/project/tmp/" + which_xml
        if not is_docker:
            which_xml = "/home/ralcraft/dev/beast-icr/xml/testStrictClock.xml"
            
        #result = subprocess.run(["/project/BEASTv1.8.4/bin/beast","-beagle_off", "-working", "-overwrite", which_xml],stdout=subprocess.PIPE)
        if is_docker:
            result = subprocess.Popen(["/project/BEASTv1.8.4/bin/beast","-beagle_off", "-working", "-overwrite", which_xml],stdout=subprocess.PIPE,shell=False)
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
            time.sleep(0.05)
        
        output  = result.stdout.readline()            
        if output :
            print(output .strip().decode('utf-8'))
        
        rc = result.poll()
        #print(result)
        #print(rc)
        return ""#result.stdout.decode('utf-8')
    except Exception as e:
        return str(e)
    

def run_pisca01(which_xml):
    """Run beast01 command."""    
    print("starting beast...")
    try:
        if which_xml == "":
            which_xml = "/project/PISCAv1.1/validation.xml"
        else:
            which_xml = "/project/tmp/" + which_xml
            
        result = subprocess.run(["/project/BEASTv1.8.4/bin/beast","-beagle_off", "-working", "-overwrite", which_xml],stdout=subprocess.PIPE)
        print(result)
        return result.stdout.decode('utf-8')
    except Exception as e:
        return str(e)
    
    