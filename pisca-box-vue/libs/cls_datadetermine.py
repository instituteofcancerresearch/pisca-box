# ruff: noqa: F841
from io import StringIO
import pandas as pd

class DataDetermine:
    """This is determines the data typer given fasta or csv input
    
    --------------------------------
    cnv
    acna
    biallelic
    phyfum
    """        
    def __init__(self, uploaded_file, type, file_name = ""):
        self.uploaded_file = uploaded_file
        self.dic_taxon_seq = {}
        self.datatype = ""
        self.file_name = file_name                    
        if uploaded_file is not None:
            self.seq_data = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
        elif file_name != "":
            with open(file_name, "r") as f:
                self.seq_data = f.read()
                
        if type == "fasta" or type == "fa":
            self._load_seq_from_fasta()
        else:
            if self._first_row_index():
                self._load_seq_from_csv()
            else:
                self._load_seq_from_csv_row()
        self._determine_datatype()        
    ##############################################################        
    def get_seq_data(self):
        return self.dic_taxon_seq, self.datatype
    ##############################################################
    def _first_row_index(self):
        ls_string = self.seq_data.split("\n")
        for row in ls_string:
            if row.startswith(","):
                return True
            else:
                return False
    ##############################################################
    def _determine_datatype(self):
        len_set = 0
        comma = False
        dot = False
        for taxon in self.dic_taxon_seq:
            seqq = self.dic_taxon_seq[taxon]
            to_set = set(self.dic_taxon_seq[taxon])
            len_set = max(len_set,len(to_set))
            if "," in seqq:
                comma = True
            if "." in seqq:
                dot = True
        if dot:
            self.datatype = "phyfum"
        else:
            if comma:
                len_set -= 1
            if len_set <= 3:
                self.datatype = "biallelic"
            elif len_set <= 10:
                self.datatype = "acna"
            else:
                self.datatype = "cnv"
        convert = self.datatype in ["acna","cnv"]
        comma = not dot
        self._convert_seq_data(convert,comma)        
        if self.datatype in ["acna","cnv"]:
            not_in = False
            for taxon in self.dic_taxon_seq:
                seq = self.dic_taxon_seq[taxon]
                for ch in seq:
                    if ch not in "ABCDEFGHIJ":
                        not_in = True
                        break
            if not_in:
                self.datatype = "cnv"                                                                                    
    ##############################################################
    def _load_seq_from_fasta(self):
        ls_string = self.seq_data.split(">")
        for id_seq in ls_string:
            idseqs = id_seq.split("\n")
            if len(idseqs) < 2:                
                continue
            idd = idseqs[0].strip()
            seq = idseqs[1].strip()
            self.dic_taxon_seq[idd] = seq
    ##############################################################            
    def _load_seq_from_csv_row(self):
        """first 2 rows of data could look like
        
        acna
        IBD002_078E_S34,3,3,3,3,3,3,3,3,3,
        IBD002_083E_S18,2,2,2,2,2,2,2,2,
                        
        phyfum
        taxon8,0.919153,0.75007,0.848006,
        taxon7,0.919153,0.75007,0.848006,
        """

        ls_string = self.seq_data.split("\n")
        for row in ls_string:
            els = row.split(",")
            idd = els[0].strip()
            seq = ""
            for el in els[1:]:
                seq += el.strip()+","
            self.dic_taxon_seq[idd] = seq[:-1]
    ##############################################################
    def _load_seq_from_csv(self):
        """first 2 rows of data could look like
                       
        bb
        ,SCLL-012,SCLL-545,SCLL-546,SCLL-547,SCLL-548
        cg00405069,0,0,0,0,0
                
        """                
        if self.file_name != "":
            seq_csv = pd.read_csv(self.file_name,index_col=0)
        else:
            seq_csv = pd.read_csv(self.uploaded_file,index_col=0)
        taxa = seq_csv.columns               
        for taxon in taxa:
            taxon = taxon.strip()
            seqs = seq_csv[taxon].tolist()
            seq = ''.join(str(seqs))
            seq = seq.replace(",","").replace(" ","").replace("[","").replace("]","")            
            self.dic_taxon_seq[taxon] = seq            
    ##############################################################
    def _convert_seq_data(self,convert,comma):        
        for id,seq in self.dic_taxon_seq.items():
            if convert:
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
            if comma:
                seq = seq.replace(",","")
            self.dic_taxon_seq[id] = seq            
    