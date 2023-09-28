import test_01_beauti as beauti
import test_beauti_biallelic as bb
#import test_beauti_phyfum as phy

overwrite_new_data = False    


s1 = beauti.test_0101(show_xml=False,save_xml=True,overwrite=overwrite_new_data,check_assert = True)

s1 = bb.test_biallelic_xml(show_xml=False,save_xml=True,overwrite=overwrite_new_data,check_assert = True)

#s2 = phy.test_phyfum_xml(show_xml=False,save_xml=True,overwrite=overwrite_new_data,check_assert = True)




