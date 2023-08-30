


class Fasta(object):
    def __init__(self, big_string,dates_csv):
        self.big_string = big_string
        self.dates_csv = dates_csv
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
        self.dic_id_seq = {}        
        self.dic_id_dates = {}
        self.dic_id_tips = {}
        
        ls_string = self.big_string.split(">")
        for id_seq in ls_string:
            idseq = id_seq.split("\n")
            if len(idseq) < 2:                
                continue
            id = idseq[0].strip()
            seq = idseq[1].strip()
            self.dic_id_seq[id] = seq
        
        if self.dates_csv is not None:
            cols = self.dates_csv.columns        
            for i,row in self.dates_csv.iterrows():
                id = row[cols[0]]
                dat = row[cols[1]]
                dec = row[cols[2]]
                tip = row[cols[3]]  
                loc = row[cols[4]]
                cpt = row[cols[5]]
                #if id in self.dic_id_seq:
                self.dic_id_dates[id] = (dat,dec,tip,loc,cpt)
                self.dic_id_tips[tip] = (dat,dec,id,loc,cpt)
                    
            
            #print(self.dic_id_dates)
                
                    
    def _make_a_taxon(self,id,date,compartment):
        taxon = ""
        taxon += f'\t<taxon id="{id}">\n'
        taxon += f'\t\t<date value="{date}" direction="forwards" units="years"/>\n'
        if compartment != "?":
            taxon += f'\t\t<attr name="compartment">\n'
            taxon += f'\t\t\t{compartment}"\n'
            taxon += f'\t\t</attr>\n'            
        taxon += f'\t</taxon>\n'
        return taxon
			    
    def _make_taxa(self):
        taxa = '<taxa id="taxa">\n'
        for id,seq in self.dic_id_seq.items():
            dat,dec,tip,loc,cpt = "?","?","?","?","?"
            if id in self.dic_id_dates:
                dat,dec,tip,loc,cpt = self.dic_id_dates[id]        
            elif id in self.dic_id_tips:
                dat,dec,id2,loc,cpt = self.dic_id_tips[id]        
            else:
                print(f"Warning: {id} not found in dates file")
            taxa += self._make_a_taxon(id,dec,cpt)
        taxa += '</taxa>\n'
        return taxa
    
    def _make_a_sequence(self,id,seq):
        seqstr = "\t<sequence>\n"
        seqstr += f'\t\t<taxon idref="{id}"/>\n'
        seqstr += f'\t\t{seq}\n'
        seqstr += '\t</sequence>\n'
        return seqstr
     
    
    def _make_alignment(self,datatype):
        #<alignment id="alignment">
	    #<dataType idref="cnv"/>
        algn = '<alignment id="alignment">\n'
        algn += f'\t<dataType idref="{datatype}"/>\n'
        for id,seq in self.dic_id_seq.items():
            algn += self._make_a_sequence(id,seq)
        algn += '</alignment>\n'
        return algn
	
    