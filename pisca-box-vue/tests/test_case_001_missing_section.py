# ruff: noqa: F841
import __init__ # noqa: F401
import libs.cls_xml as xml
import libs.cls_dt_biallelic as bb
import libs.cls_operators as ops
import libs.cls_mcmc as mc
import pandas as pd
import libs.cls_priors as prs
import libs.cls_datadetermine as dd

# Raised by Heather : https://github.com/instituteofcancerresearch/pisca-box/issues/40


# The test data she gave is private and is not included in the repo

# I have created a test data set that is public and can be used to test the issue

def test_40(internal=False,show_xml=False,save_xml=False,overwrite=False,check_assert=True):
                
    trials = []
    if internal:
        trials.append(['bb-fasta','case_001/CRC-multi_patient-M.fasta','case_001/M.csv','bb'])
        trials.append(['bb-space','case_001/CRC-multi_patient-M-space.fasta','case_001/M_spaces.csv','bb'])        
        this_dir = "/".join(__file__.split('/')[:-1])
        this_dir = f'{this_dir}/internal'
    else:        
        trials.append(['bb-csv','case_001/biallelic-seq.csv','case_001/biallelic-ages.csv','bb'])
        trials.append(['bb-space','case_001/biallelic-seq-space.csv','case_001/biallelic-ages-space.csv','bb'])
        this_dir = "/".join(__file__.split('/')[:-1])
        this_dir = f'{this_dir}/external'
                
    for key,seq_file,seq_ages,seq_type in trials:
                              
        file_name = f'{this_dir}/{seq_file}'                
        nm,tp = file_name.lower().split(".")
        dtd = dd.DataDetermine(None,tp,file_name)
        dic_seq,dtyp = dtd.get_seq_data()
        
        # ages selection - we want the column with age as the header        
        csv_ages = pd.read_csv(f'{this_dir}/{seq_ages}')
                                                                        
        # CLOCK        
        clock = "strict clock" # ["strict clock", "random local clock"]
        clock_rate = 0.13
        clocks = {}        
        clocks['type'] = clock
        clocks['rate'] = clock_rate
        
        
        # LUCA        
        max_age = csv_ages['age'].max()   
        min_age = csv_ages['age'].min()
        lucas = {}
        lucas["model"] = "Neoplastic progression"
        lucas["hvalue"] = max_age
        lucas["hupper"] = 0
        lucas["hlower"] = min_age
        lucas["bvalue"] = 1
        lucas["bupper"] = min_age
        lucas["blower"] = 0     
                
        # TREES
        demographic =  "constant size" #["constant size", "exponential growth"]
        
        # MCMC
        mcmcs = {}
        mcmcs['name'] = "my name any"
        mcmcs['chain_length'] = 2500
        mcmcs['log_every'] = 250
        mcmcs['mle'] = True
                
        # PRIORS
        priors = {}
        priors['luca_branch'] = {'prior_type':'uniform','value':max_age}
        priors['clock.rate'] = {'prior_type':'normal','mean':0.0,'std':0.13}
        priors['biallelicBinary.demethylation'] = {'prior_type':'logNormal','mean':1.0,'std':0.6,'offset':0.0,'realSpace':True}
        priors['biallelicBinary.homozygousMethylation'] = {'prior_type':'logNormal','mean':1.0,'std':0.6,'offset':0.0,'realSpace':True}
        priors['biallelicBinary.homozygousDemethylation']= {'prior_type':'logNormal','mean':1.0,'std':0.6,'offset':0.0,'realSpace':True} 
        
        # Load DATATYPE
        dt_obj =  bb.Biallelic(dic_seq,csv_ages)
        operators = ops.Operators(demographic,lucas["model"],clocks,dt_obj.ops)
        prrs = prs.Priors(demographic,dt_obj.prs)
        mcmc = mc.MCMC(mcmcs,clocks,prrs,dt_obj,operators,[])
        xmlwriter = xml.XmlWriter(dt_obj,mcmc,lucas,clocks,demographic,dt_obj,operators)
                                                
        xmlstr = xmlwriter.get_xml()
        if show_xml:
            print(xmlstr)
        if save_xml:
            filename = f'{this_dir}/{seq_file}_fix.xml'
            if not overwrite:
                filename = f'{this_dir}/{seq_file}_tst.xml'                
            with open(filename, "w") as f:
                f.write(xmlstr)
                print("saved to",filename)
        xmlstr = xmlstr.replace("\n","").replace(" ","").replace("\t","")
        if check_assert:
            fix_file = f'{this_dir}/{seq_file}_fix.xml'
            fix_str = ""
            with open(fix_file, "r") as f:
                fix_str = f.read()
            fix_str = fix_str.replace("\n","").replace(" ","").replace("\t","")
            
            
            assert fix_str == xmlstr, f"BEAUTI-01 xml strings do not match for {seq_file}"
        
        
        
    

##########################
if __name__ == "__main__":
    test_40(internal=True,show_xml=False,save_xml=True,overwrite=False,check_assert=True)
    test_40(internal=False,show_xml=False,save_xml=True,overwrite=False,check_assert=True)
    
    
    
