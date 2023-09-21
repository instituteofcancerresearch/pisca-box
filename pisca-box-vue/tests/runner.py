import os
import glob
import test_01_beauti as beauti
import regression_01_beast as beast

def run_regression():

    # These are run in continuous integration
    ################################################# UNIT #################################################

    ################################################# BEAUTI #################################################
    #create new fixtures file
    #beauti.test_0101(show_xml=False,save_xml=True,overwrite=True,check_assert = True)
    #check existing fixtures file against test
    s1 = beauti.test_0101(show_xml=False,save_xml=True,overwrite=False,check_assert = True)



    # These require beast and psica and java install and are run as regression tests
    ################################################# BEAST #################################################
    s2 = beast.reg_0201()
    
    return s1 and s2
    
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
        except:
            print("Error while deleting file : ", filePath)
    


