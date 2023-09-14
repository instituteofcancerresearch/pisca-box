import pandas as pd


class Fasta(object):
    def __init__(self, big_string,ages_csv,seq_conversion,taxon_csv=pd.DataFrame()):
        self.big_string = big_string
        self.ages_csv = ages_csv
        self.seq_conversion = seq_conversion
        self.taxon_csv = taxon_csv        
        self._convert_to_dict()
        
    ### PUBLIC INTERFACE ######### 
    def get_fasta(self):
        return self.big_string
    
    def get_fasta_taxa(self):
        return self._make_taxa()
    
    def get_fasta_alignment(self,datatype):
        return self._make_alignment(datatype)
    
    ### PRIVATE HELPERS ######### 
    
    def _convert_to_dict(self):
        self.dic_taxon_age = {}
        self.dic_taxon_seq = {}
        self.dic_taxon_compartment = {}
        
        if self.taxon_csv.empty:
            ls_string = self.big_string.split(">")
            for id_seq in ls_string:
                idseq = id_seq.split("\n")
                if len(idseq) < 2:                
                    continue
                id = idseq[0].strip()
                seq = idseq[1].strip()
                if self.seq_conversion:
                    seq = seq.replace("0","A")
                    seq = seq.replace("1","B")
                    seq = seq.replace("2","C")
                    seq = seq.replace("3","D")
                    seq = seq.replace("4","E")
                    seq = seq.replace("5","F")
                    seq = seq.replace("6","G")
                    seq = seq.replace("7","H")
                    seq = seq.replace("8","I")
                    seq = seq.replace("9","J")
                self.dic_taxon_seq[id] = seq
        else:
            taxa = self.taxon_csv.columns            
            for taxon in taxa:
                taxon = taxon.strip()
                seqs = self.taxon_csv[taxon].tolist()
                seq = ''.join(str(seqs))
                seq = seq.replace(",","").replace(" ","").replace("[","").replace("]","")                
                if self.seq_conversion:
                    seq = seq.replace("0","A")
                    seq = seq.replace("1","B")
                    seq = seq.replace("2","C")
                    seq = seq.replace("3","D")
                    seq = seq.replace("4","E")
                    seq = seq.replace("5","F")
                    seq = seq.replace("6","G")
                    seq = seq.replace("7","H")
                    seq = seq.replace("8","I")
                    seq = seq.replace("9","J")
                self.dic_taxon_seq[taxon] = seq
        
        
        if self.ages_csv is not None:
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
            if id in self.dic_taxon_compartment:
                cpt = self.dic_taxon_compartment[id]        
            else:
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
     
    
    def _make_alignment(self,datatype):        
        algn = '<alignment id="alignment">\n'
        algn += f'\t<dataType idref="{datatype}"/>\n'
        for id,seq in self.dic_taxon_seq.items():
            algn += self._make_a_sequence(id,seq)
        algn += '</alignment>\n'
        return algn
	
    