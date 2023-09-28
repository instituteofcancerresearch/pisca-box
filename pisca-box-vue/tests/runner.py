import os
import glob
import test_01_beauti as beauti
import regression_01_beast as beast
import test_beauti_biallelic as bb
import test_beauti_phyfum as phy

def run_regression():

    # These are run in continuous integration
    ################################################# UNIT #################################################

    ################################################# BEAUTI #################################################
    #create new fixtures file
    overwrite_new_data = False    
    s1 = beauti.test_0101(show_xml=False,save_xml=True,overwrite=overwrite_new_data,check_assert = True)
    s2 = bb.test_biallelic_xml(show_xml=False,save_xml=True,overwrite=overwrite_new_data,check_assert = True)
    s3 = bb.test_phyfum_xml(show_xml=False,save_xml=True,overwrite=overwrite_new_data,check_assert = True)


    # These require beast and psica and java install and are run as regression tests
    ################################################# BEAST #################################################
    s4 = beast.reg_0201()
    
    return s1 and s2 and s3 and s4
    
def run_beast_regression():        
    # Running tests in the container - built in the previous step of the build process
    ################################################# BEAST #################################################
    s2 = beast.reg_0202()
    
    return s2

def clean_logs(dir,pattern):    
    # Get a list of all the file paths that ends with .txt from in specified directory
    fileList = glob.glob(f'{dir}/{pattern}')
    # Iterate over the list of filepaths & remove each file.
    for filePath in fileList:
        try:
            os.remove(filePath)
            print("Removed : ", filePath)
        except Exception as e:
            print("Error while deleting file : ", filePath,str(e))
    


