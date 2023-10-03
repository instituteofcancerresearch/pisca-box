#https://stackoverflow.com/questions/372042/difference-between-abstract-class-and-interface-in-python
#https://www.w3schools.com/python/python_inheritance.asp


class DataType:
    """This is an abstract class for the datatypes. 
    Some hlper functions are implemented here
    
    functions starting _ are intended to be private
    --------------------------------
    cnv
    acna
    biallelic
    phyfum
    """    
    ## inherited class init ##########################################
    """
    def __init__(self,seq_data_dic,ages_csv):
        super().__init__(seq_data_dic,ages_csv)
    """        
    ## abstract class init ##########################################
    def __init__(self,seq_data_dic,ages_csv):
        self.ages_csv = ages_csv
        self.dic_taxon_seq = seq_data_dic
        self.dic_taxon_age = {}
        self.dic_taxon_compartment = {}
        self.datatype = self._get_datatype()        
        self._load_ages_data()
        self.ops = self._default_operators()
        self.prs = self._default_priors()
    ##############################################################
    # ABSTRACT FUNCTIONS TO IMPLEMENT
    ##############################################################                    
    def _get_datatype(self):
        raise NotImplementedError("Should have implemented this")        
    ##############################################################                    
    def _load_data(self):
        raise NotImplementedError("Should have implemented this")
    ##############################################################
    def _default_operators(self):
        raise NotImplementedError("Should have implemented this")
    #############################################################
    def _default_priors(self):
        raise NotImplementedError("Should have implemented this")
    #############################################################
    ## XML ##
    def get_datatype_xml(self):
        raise NotImplementedError("Should have implemented this")
    ##############################################################                    
    def get_site_model(self):
        raise NotImplementedError("Should have implemented this")
    ##############################################################
    def get_character_patterns(self):
        raise NotImplementedError("Should have implemented this")
    ##############################################################
    def get_frequency_model(self):
        raise NotImplementedError("Should have implemented this")
    ##############################################################
    def get_cna_model(self):
        raise NotImplementedError("Should have implemented this")
    ##############################################################
    
    
    ##############################################################
    # IMPLEMENTED HELPER FUNCTIONS
    ##############################################################                                                                        
    def get_min_max_ages(self):
        return self.ages_csv['age'].min(), self.ages_csv['age'].max()
    ##############################################################                                                                        
    def get_fasta_taxa(self):
        return self._make_taxa()
    ##############################################################                                                                        
    def get_fasta_alignment(self):
        return self._make_alignment()        
    ##############################################################                    
    def _make_a_taxon(self,id,age,compartment):
        taxon = ""
        taxon += f'\t<taxon id="{id}">\n'
        taxon += f'\t\t<date value="{age}" direction="forwards" units="years"/>\n'
        if compartment != "?":
            taxon += '\t\t<attr name="compartment">\n'
            taxon += f'\t\t\t{compartment}"\n'
            taxon += '\t\t</attr>\n'            
        taxon += '\t</taxon>\n'
        return taxon
    ##############################################################
    def _make_taxa(self):
        taxa = '<taxa id="taxa">\n'
        cpt = "?"      
        for tx,age in self.dic_taxon_age.items():            
            if tx in self.dic_taxon_compartment:
                cpt = self.dic_taxon_compartment[tx]                    
            if tx in self.dic_taxon_seq:
                taxa += self._make_a_taxon(tx,age,cpt)
            # don't use it otherwise as there is no seq data
        taxa += '</taxa>\n'
        return taxa
    ##############################################################
    def _make_a_sequence(self,id,seq):
        seqstr = "\t<sequence>\n"
        seqstr += f'\t\t<taxon idref="{id}"/>\n'
        seqstr += f'\t\t{seq}\n'
        seqstr += '\t</sequence>\n'
        return seqstr
    ##############################################################    
    def _make_alignment(self):        
        algn = '<alignment id="alignment">\n'
        algn += f'\t<dataType idref="{self.datatype}"/>\n'
        for id,seq in self.dic_taxon_seq.items():
            if id in self.dic_taxon_age:
                algn += self._make_a_sequence(id,seq.strip())        
            # don't use it otherwise as there is no age data
        algn += '</alignment>\n'
        return algn        
    ##############################################################
    def _load_ages_data(self):        
        ages = self.ages_csv["age"]
        taxa = self.ages_csv["taxon"]
        for i in range(len(ages)):
            taxon = taxa[i]
            age = ages[i]
            self.dic_taxon_age[taxon] = age     
        if "compartment" in self.ages_csv.columns:
            compartments = self.ages_csv["compartment"]
            taxa = self.ages_csv["taxon"]
            for i in range(len(compartments)):
                taxon = taxa[i]
                cpt = compartments[i]
                self.dic_taxon_compartment[taxon] = cpt
    ##############################################################
        
	
    

    