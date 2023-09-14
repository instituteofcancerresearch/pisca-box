import test_01_beauti as beauti


################################################# BEAUTI #################################################
#### CHECK THE BEAUTI FILES ARE THE SAME
#create new fixtures file
#beauti.test_0101(show_xml=False,save_xml=True,overwrite=True,check_assert = True)
#check existing fixtures file against test
beauti.test_0101(show_xml=False,save_xml=True,overwrite=False,check_assert = True)

#### CHECK THE FASTA AND CSV VERSIONS ARE GIVING THE SAME RESULTS
beauti.test_0102()



################################################# PISCA #################################################

