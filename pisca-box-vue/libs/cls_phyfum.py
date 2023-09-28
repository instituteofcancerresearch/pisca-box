# ruff: noqa
import pandas as pd


class Phyfum(object):
    def __init__(self, decimal_file, ages_file):
        self.datatype = "phyfum"
        self.decimal_file = decimal_file
        self.ages_file = ages_file
        self.dic_taxon_age = {}
        self.dic_taxon_seq = {}
        self.min_age = -1
        self.max_age = -1
        
        self._load_data()
                
    ### PUBLIC INTERFACE #########         
    def get_fasta_taxa(self):
        return self._make_taxa()
    
    def get_fasta_alignment(self,data_type):
        return self._make_alignment()
    
    def get_min_max_ages(self):
        return self.min_age, self.max_age
    
    ### PRIVATE HELPERS #########                                                         
    def _load_data(self):        
        lines = []
        with open(self.decimal_file, "r") as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line == "":
                continue
            pos = line.find(",") #we obnly want the first column
            if pos > 0:
                idd = line[:pos]
                seq = line[pos+1:]
                self.dic_taxon_seq[idd] = seq                
        # ages selection - we want the column with age as the header        
        csv_ages = pd.read_csv(self.ages_file)
        self.max_age = csv_ages['age'].max()   
        self.min_age = csv_ages['age'].min()
        ages = csv_ages["age"]
        taxa = csv_ages["taxon"]
        for i in range(len(ages)):
            taxon = taxa[i]
            age = ages[i]
            self.dic_taxon_age[taxon] = age                                                
        
                                
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

    def _make_taxa(self):
        taxa = '<taxa id="taxa">\n'        
        for tx,age in self.dic_taxon_age.items():            
            if id in self.dic_taxon_seq:
                cpt = self.dic_taxon_seq[id]        
            else:
                cpt = "?"            
            taxa += self._make_a_taxon(tx,age,cpt)
        taxa += '</taxa>\n'
        return taxa
    
    def _make_a_sequence(self,id,seq):
        seqstr = "\t<afsequence>\n"
        seqstr += f'\t\t<taxon idref="{id}"/>\n'
        seqstr += f'\t\t{seq}\n'
        seqstr += '\t</afsequence>\n'
        return seqstr
     
    
    def _make_alignment(self):        
        algn = '<afalignment id="alignment">\n'
        algn += f'\t<dataType idref="{self.datatype}"/>\n'
        for id,seq in self.dic_taxon_seq.items():
            algn += self._make_a_sequence(id,seq.strip())
        algn += f'\t<stemCells>\n'
        algn += f'\t\t<parameter id="alignment.stemCells" value="3"/>\n'
        algn += f'\t</stemCells>\n'
        algn += '</afalignment>\n'
        return algn
	
    