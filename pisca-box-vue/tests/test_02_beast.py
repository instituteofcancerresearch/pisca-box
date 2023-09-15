import __init__ # noqa: F401
import libs.cmds as cmd

this_dir = "/".join(__file__.split('/')[:-1])

def test_0201():
    xmls = []
    xmls.append("data_02a_validation_fix.xml")
        
    for xml in xmls:
        filename = f'{this_dir}/fixtures/{xml}'
                
        paramstr = f"-working,-overwrite,-beagle_off,{filename}"
        params = paramstr.split(",")                
        cmd.run_beast(params)
    
    
    
    