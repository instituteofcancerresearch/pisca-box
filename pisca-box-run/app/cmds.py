import subprocess

def run_validation(dir):
    """Run validation command."""    
    print("listing files...")
    #result01 = subprocess.run(["ls","-l"],stdout=subprocess.PIPE)
    result01 = subprocess.run(["pwd"],stdout=subprocess.PIPE)
    #result03 = subprocess.run(["ls","/project"],stdout=subprocess.PIPE)
    result02 = subprocess.run(["ls",dir,"-l"],stdout=subprocess.PIPE)
    
    return result01.stdout.decode('utf-8') + "\n" + result02.stdout.decode('utf-8')



def run_beast01(which_xml):
    """Run beast01 command."""    
    print("starting beast...")
    try:
        if which_xml == "":
            which_xml = "/project/BEASTv1.8.4/examples/testXML/testLikelihood.xml"
        else:
            which_xml = "/project/tmp/" + which_xml
        result = subprocess.run(["/project/BEASTv1.8.4/bin/beast","-beagle_off", "-working", "-overwrite", which_xml],stdout=subprocess.PIPE)
        print(result)
        return result.stdout.decode('utf-8')
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
    
    