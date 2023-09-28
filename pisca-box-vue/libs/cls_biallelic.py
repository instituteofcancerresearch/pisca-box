import pandas as pd

class Biallelic(object):
    def __init__(self, seq_data, seq_csv,ages_csv):
        self.datatype = "biallelicBinary"
        self.seq_data = seq_data
        self.seq_csv = seq_csv
        self.ages_csv = ages_csv
        self.dic_taxon_age = {}
        self.dic_taxon_seq = {}
        self.dic_taxon_compartment = {}
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
        if self.seq_data == "":            
            taxa = self.seq_csv.columns               
            for taxon in taxa:
                taxon = taxon.strip()
                seqs = self.seq_csv[taxon].tolist()
                seq = ''.join(str(seqs))
                seq = seq.replace(",","").replace(" ","").replace("[","").replace("]","")                                                
                self.dic_taxon_seq[taxon] = seq            
        else:            
            ls_string = self.seq_data.split(">")
            for id_seq in ls_string:
                idseq = id_seq.split("\n")
                if len(idseq) < 2:                
                    continue
                id = idseq[0].strip()
                seq = idseq[1].strip()                                
                self.dic_taxon_seq[id] = seq                
        # ages selection - we want the column with age as the header                
        self.max_age = self.ages_csv['age'].max()   
        self.min_age = self.ages_csv['age'].min()
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
            #if id in self.dic_taxon_seq:
            #    seq = self.dic_taxon_seq[id]        
            #else:
            cpt = "?"            
            taxa += self._make_a_taxon(tx,age,cpt)
        taxa += '</taxa>\n'
        return taxa
    
    def _make_a_sequence(self,id,seq):
        seqstr = "\t<sequence>\n"
        seqstr += f'\t\t<taxon idref="{id}"/>\n'
        seqstr += f'\t\t{seq}\n'
        seqstr += '\t</sequence>\n'
        return seqstr
     
    
    def _make_alignment(self):        
        algn = '<alignment id="alignment">\n'
        algn += f'\t<dataType idref="{self.datatype}"/>\n'
        for id,seq in self.dic_taxon_seq.items():
            algn += self._make_a_sequence(id,seq.strip())        
        algn += '</alignment>\n'
        return algn
	
    