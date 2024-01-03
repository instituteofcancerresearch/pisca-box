# ruff: noqa: F841
import __init__ # noqa: F401
import libs.cmds as cmd

this_dir = "/".join(__file__.split('/')[:-1])
                                        
def test_pisca_box(show_xml=False,save_xml=False,overwrite=False,check_assert = True):
    success = True
         
    trials = []        
    trials.append('validation/val_fix.xml')
                
    for xml_file in trials:
                              
        file_name = f'{this_dir}/fixtures/{xml_file}'                        
        params = ["-working", "-overwrite", "-beagle_off"]                
        params.append(file_name)
        
        try:                    
            ret  = cmd.run_beast(params)
            assert ret == "done"
        except Exception as E:
            print("If BEAST is not installed don't regression it")                                            
           
############################################    

if __name__ == "__main__":
    #test_biallelic_xml(show_xml=False,save_xml=True,overwrite=True,check_assert = True)
    test_pisca_box(show_xml=False,save_xml=False,overwrite=False,check_assert = True)

    
    
