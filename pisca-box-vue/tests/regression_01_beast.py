import __init__ # noqa: F401
import libs.cmds as cmd
import subprocess


this_dir = "/".join(__file__.split('/')[:-1])

def reg_0201():
    success = True
    xmls = []
    xmls.append("validation/val_fix.xml")
        
    for xml in xmls:
        filename = f'{this_dir}/fixtures/{xml}'
                
        paramstr = f"-working,-overwrite,-beagle_off,{filename}"
        params = paramstr.split(",")                
        ret = cmd.run_beast(params)
        assert ret == "done", "beast failed"
        if ret != "done":
            success = False
    return success

def reg_0202():
    # regular beast run
    #docker run -v ~/dev/beast-icr/xml:/project/xml pisca-box validation.xml
    cmd_one = "docker run -v ~/dev/beast-icr/pisca-box/pisca-box-vue/tests/fixtures:/mnt --rm pisca-box-run data_02a_validation_fix.xml"
    result = subprocess.run(cmd_one,stdout=subprocess.PIPE,shell=True,).stdout.decode('utf-8')            
    print(result.strip())
        
    
    
    
    
    