import __init__ # noqa: F401
import libs.cls_xml as xml
import libs.cls_fasta as fa
import libs.cls_mcmc as mc
import libs.cls_operators as ops
import pandas as pd

this_dir = "/".join(__file__.split('/')[:-1])


def help_show_dif(stringa, stringb):
    min_len = min(len(stringa),len(stringb))
    for i in range(min_len):
        if stringa[i] != stringb[i]:
            print(i,stringa[i],stringb[i])
            if i > 5 and i < min_len - 5:
                print(i,stringa[i-3:i+3],stringb[i-3:i+3])
    
                        
def test_0101(show_xml=False,save_xml=False,overwrite=False,check_assert = True):
    success = True
         
    trials = []
    trials.append(['set1','data_01a_belle.fasta','data_01a_belle_dates.csv','cnv',False])
    #trials.append(['bb-fasta','data_01b_patient1.fasta','data_01b_patient1_bb_orig_ages.csv','bb',False])
    #trials.append(['bb-csv','data_01b_patient1_bb_seq.csv','data_01b_patient1_bb_orig_ages.csv','bb',True])
            
    for key,seq_file,seq_ages,seq_type,as_csv in trials:

        # File selection
        fasta_string = ""
        seq_csv = pd.DataFrame()        
        if not as_csv:
            with open(f'{this_dir}/fixtures/{seq_file}', "r") as f:
                fasta_string = f.read()
        else:
            seq_csv = pd.read_csv(f'{this_dir}/fixtures/{seq_file}',index_col=0)
            
        # ages selection - we want the column with age as the header        
        csv_ages = pd.read_csv(f'{this_dir}/fixtures/{seq_ages}')
                        
        # PISCA
        datatype = seq_type #(cnv / acna / bb)
        seq_conversion = datatype in ['cnv','acna']   
        
        # CLOCK        
        clock = "strict clock" # ["strict clock", "random local clock"]
        clock_rate = 0.13
        clocks = {}        
        clocks['type'] = clock
        clocks['rate'] = clock_rate
        
        
        # LUCA
        #we want to draw the age
        # 
        # 
        # s from column age and the seq id from column taxon
        max_age = csv_ages['age'].max()   
        min_age = csv_ages['age'].min()
        lucas = {}
        lucas["height"] = max_age
        lucas["branch"] = 34
        lucas["lower"] = 0.0
        lucas["upper"] = min_age                
                
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
        
                                
        operators = ops.Operators(demographic,datatype,clocks)
        fasta = fa.Fasta(fasta_string,csv_ages,seq_conversion,seq_csv)
        mcmc = mc.MCMC(mcmcs,clocks,priors)                                    
        xmlwriter = xml.XmlWriter(fasta,mcmc,lucas,clocks,demographic,datatype,operators)

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
        
        
    return success
            
           
############################################    

#def test_0102():    
#    # these files should be the same
#    trials = []
#    trials.append(['data_01b_patient1.fasta_tst.xml','data_01b_patient1_bb_seq.csv_tst.xml'])
#    
#    for filea,fileb in trials:
#        with open(f'{this_dir}/fixtures/{filea}', "r") as f:
#            filea_str = f.read()
#        filea_str = filea_str.replace("\n","").replace(" ","").replace("\t","")
#                
#        with open(f'{this_dir}/fixtures/{fileb}', "r") as f:
#            fileb_str = f.read()
#        fileb_str = fileb_str.replace("\n","").replace(" ","").replace("\t","")
#        
#        if filea_str != fileb_str:
#            help_show_dif(filea_str,fileb_str)                                                         
#        assert filea_str == fileb_str, f"BEAUTI-02 xml files do not match for {filea} and {fileb}"
    
    
