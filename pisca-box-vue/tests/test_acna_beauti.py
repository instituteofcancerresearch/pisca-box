# ruff: noqa: F841
import __init__ # noqa: F401
import libs.cls_xml as xml
import libs.cls_mcmc as mc
import libs.cls_operators as ops
import pandas as pd
import libs.cls_datadetermine as dd
import libs.cls_dt_biallelic as bb
import libs.cls_dt_acna as ac
import libs.cls_dt_cnv as cv
import libs.cls_dt_phyfum as phy
import libs.cls_priors as prs

this_dir = "/".join(__file__.split('/')[:-1])


def help_show_dif(stringa, stringb):
    stringsa = stringa.split("/>")
    stringsb = stringb.split("/>")
    min_len = min(len(stringsa),len(stringsb))
    for i in range(min_len):
        stringa = stringsa[i].strip()
        stringb = stringsb[i].strip()
        if stringa != stringb:
            print("LINE=",i,stringa,stringb)
            print("-----")
            print(stringa)
            print("-----")
            print(stringb)
            print("-----")
                                        
def test_0101(show_xml=False,save_xml=False,overwrite=False,check_assert = True):
    success = True
         
    trials = []
    trials.append(['set1','acna/acna.fasta','acna/acna_dates.csv','acna',False])
    trials.append(['set2','acna/acna.csv','acna/acna_dates.csv','acna',False])
    
                
    for key,seq_file,seq_ages,seq_type,as_csv in trials:

        # File selection
        fasta_string = ""
        seq_csv = pd.DataFrame()
        file_name = f'{this_dir}/fixtures/{seq_file}'                
        nm,tp = file_name.lower().split(".")
        dtd = dd.DataDetermine(None,tp,file_name)
        dic_seq,dtyp = dtd.get_seq_data()
        
        # ages selection - we want the column with age as the header        
        csv_ages = pd.read_csv(f'{this_dir}/fixtures/{seq_ages}')
        
        if dtyp == 'biallelic':
            dt_obj =  bb.Biallelic(dic_seq,csv_ages)
        elif dtyp == 'acna':
            dt_obj =  ac.Acna(dic_seq,csv_ages)
        elif dtyp == "cnv":
            dt_obj =  cv.Cnv(dic_seq,csv_ages)
        elif dtyp == "phyfum":
            dt_obj =  phy.Phyfum(dic_seq,csv_ages)
        else:
            print("Unrecognised datatype",dtyp)
                                                                                                    
        # TREES
        demographic =  "constant size" #["constant size", "exponential growth"]
        
        # MCMC
        mcmcs = {}
        mcmcs['name'] = "my name any"
        mcmcs['chain_length'] = 2500
        mcmcs['log_every'] = 250
        mcmcs['mle'] = True
        
        # clocks
        clocks = {}        
        clocks['type'] = "strict clock"
        clocks['rate'] = 1.0
                
        max_age = csv_ages['age'].max()   
        min_age = csv_ages['age'].min()
        lucas = {}
        lucas["height"] = max_age
        lucas["branch"] = 34
        lucas["lower"] = 0.0
        lucas["upper"] = min_age     
                
                                                        
        operators = ops.Operators(demographic,clocks,dt_obj.ops)
        prrs = prs.Priors(demographic,dt_obj.prs)
        mcmc = mc.MCMC(mcmcs,clocks,prrs,dt_obj,operators,[])
        xmlwriter = xml.XmlWriter(dt_obj,mcmc,lucas,clocks,demographic,dt_obj,operators)

        xmlstr = xmlwriter.get_xml()
        if show_xml:
            print(xmlstr)
        if save_xml:
            filename = f'{this_dir}/fixtures/{seq_file}_fix.xml'
            if not overwrite:
                filename = f'{this_dir}/fixtures/{seq_file}_tst.xml'                
            with open(filename, "w") as f:
                f.write(xmlstr)
                print("saved to",filename)
        xmlstr = xmlstr.replace("\n","").replace(" ","").replace("\t","")
        if check_assert:
            fix_file = f'{this_dir}/fixtures/{seq_file}_fix.xml'
            fix_str = ""
            with open(fix_file, "r") as f:
                fix_str = f.read()
            fix_str = fix_str.replace("\n","").replace(" ","").replace("\t","")
            
            if fix_str != xmlstr:
                help_show_dif(fix_str,xmlstr)
                success = False
            assert fix_str == xmlstr, f"BEAUTI-01 xml strings do not match for {seq_file}"
        
            
if __name__ == "__main__":
    #test_0101(show_xml=False,save_xml=True,overwrite=True,check_assert = True)
    test_0101(show_xml=False,save_xml=False,overwrite=False,check_assert = True)
            
           
