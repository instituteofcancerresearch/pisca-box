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
    
#run_regression()


