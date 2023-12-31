tab1 = ""
tab2 = "\t"
tab3 = "\t\t"
tab4 = "\t\t\t"
tab5 = "\t\t\t\t"

class MCMC(object):
    def __init__(self, mcmcs,clocks,priors,datatype,operators,log_choices):
        self.mcmcs = mcmcs
        self.clocks = clocks
        self.priors = priors
        self.datatype = datatype
        self.operators = operators
        self.log_choices = log_choices
        
        
    ### PUBLIC INTERFACE ######### 
    def get_mcmc(self):   
        mcmc = ""         
        mcmc += f'{tab1}<mcmc id="mcmc" chainLength="{self.mcmcs["chain_length"]}" autoOptimize="true" operatorAnalysis="{self.mcmcs["name"]}.ops">\n'
        mcmc += f'{tab2}<posterior id="posterior">\n'
        ##############################################################
        ## HARDCODED AND USER PRIORS
        mcmc += self.priors.get_priors_xml()       
        ##############################################################
        mcmc += f'{tab3}<likelihood id="likelihood">\n'
        mcmc += f'{tab4}<cenancestorTreeLikelihood idref="treeLikelihood"/>\n'
        mcmc += f'{tab3}</likelihood>\n'
        mcmc += f'{tab2}</posterior>\n'
        mcmc += f'{tab2}<operators idref="operators"/>\n'
        
        # LOGGING created from priors and operators #################        
        log_list = self.datatype.selected_logs(self.priors,self.operators,self.log_choices)
        # Create log to screen ####################################
        mcmc += f'{tab2}<!-- write log to screen -->\n'
        mcmc += f'{tab2}<log id="screenLog" logEvery="{self.mcmcs["log_every"]}">\n'
        #mcmc += f'{tab3}<column label="Posterior" dp="4" width="12">\n'
        #mcmc += f'{tab4}<posterior idref="posterior"/>\n'
        #mcmc += f'{tab3}</column>\n'
        #mcmc += f'{tab3}<column label="Prior" dp="4" width="12">\n'
        #mcmc += f'{tab4}<prior idref="prior"/>\n'
        #mcmc += f'{tab3}</column>\n'
        #mcmc += f'{tab3}<column label="Likelihood" dp="4" width="12">\n'
        #mcmc += f'{tab4}<likelihood idref="likelihood"/>\n'
        #mcmc += f'{tab3}</column>\n'                                
        for prior,kind in log_list.items():
            prior_ = prior.replace(".","_")
            mcmc += f'{tab3}<column label="{prior_}" sf="6" width="12">\n'
            mcmc += f'{tab4}<{kind} idref="{prior}"/>\n'
            mcmc += f'{tab3}</column>\n'               
        mcmc += f'{tab2}</log>\n'        
        # Create log to file ####################################
        mcmc += f'{tab2}<!-- write log to file  -->\n'
        mcmc += f'{tab2}<log id="fileLog" logEvery="{self.mcmcs["log_every"]}" fileName="{self.mcmcs["name"]}.log" overwrite="false">\n'
        #mcmc += f'{tab3}<posterior idref="posterior"/>\n'
        #mcmc += f'{tab3}<prior idref="prior"/>\n'
        #mcmc += f'{tab3}<likelihood idref="likelihood"/>\n'
        for prior,kind in log_list.items():
            mcmc += f'{tab3}<{kind} idref="{prior}"/>\n'
       
        if self.clocks['type'] == "random local clock":
            mcmc += f'{tab3}<statistic idref="rateChanges"/>\n'
            mcmc += f'{tab3}<rateStatisticCenancestor idref="coefficientOfVariation"/>\n'
            mcmc += f'{tab3}<rateCovarianceStatistic idref="covariance"/>\n'
            mcmc += f'{tab3}<rateStatisticCenancestor idref="cenancestorRate"/>\n'                    
        mcmc += f'{tab2}</log>\n'
        ######################################################

        mcmc += f'{tab2}<!-- write tree log to file   -->\n'
        mcmc += f'{tab2}<logTree id="treeFileLog" logEvery="{self.mcmcs["log_every"]}" nexusFormat="true" fileName="{self.mcmcs["name"]}.trees" sortTranslationTable="true">\n'
        mcmc += f'{tab3}<treeModel idref="treeModel"/>\n'        
        if self.clocks['type'] == "random local clock":
            mcmc += f'{tab3}<trait name="rate" tag="rate">\n'
            mcmc += f'{tab4}<randomLocalClockModelCenancestor idref="branchRates"/>\n'
            mcmc += f'{tab3}</trait>\n'
            mcmc += f'{tab3}<trait name="rates" tag="relRates">\n'        
            mcmc += f'{tab4}<randomLocalClockModelCenancestor idref="branchRates"/>\n'
            mcmc += f'{tab3}</trait>\n'
            mcmc += f'{tab3}<trait name="rateIndicator" tag="indicator">\n'
            mcmc += f'{tab4}<randomLocalClockModelCenancestor idref="branchRates"/>\n'
            mcmc += f'{tab3}</trait>\n'
        elif self.clocks['type'] == "strict clock":
            mcmc += f'{tab3}<trait name="rate" tag="rate">\n'
            mcmc += f'{tab4}<strictClockCenancestorBranchRates idref="branchRates"/>\n'
            mcmc += f'{tab3}</trait>\n'
        mcmc += f'{tab3}<posterior idref="posterior"/>\n'
        mcmc += f'{tab2}</logTree>\n'
        mcmc += f'{tab1}</mcmc>\n'        
        if self.mcmcs['mle']:
            mcmc += f'{tab1}<!-- MARGINAL LIKELIHOOD ESTIMATOR -->\n'
            mcmc += f'{tab1}<!-- Define marginal likelihood estimator (PS/SS) settings -->\n'
            mcmc += f'{tab1}<marginalLikelihoodEstimator chainLength="250000" pathSteps="50" pathScheme="betaquantile" alpha="0.3">\n'
            mcmc += f'{tab2}<samplers>\n'
            mcmc += f'{tab3}<mcmc idref="mcmc"/>\n'
            mcmc += f'{tab2}</samplers>\n'
            mcmc += f'{tab2}<pathLikelihood id="pathLikelihood">\n'
            mcmc += f'{tab3}<source>\n'
            mcmc += f'{tab4}<posterior idref="posterior"/>\n'
            mcmc += f'{tab3}</source>\n'
            mcmc += f'{tab4}<destination>\n'
            mcmc += f'{tab4}<prior idref="prior"/>\n'
            mcmc += f'{tab3}</destination>\n'
            mcmc += f'{tab2}</pathLikelihood>\n'
            mcmc += f'{tab2}<log id="MLELog" logEvery="1000" fileName="{self.mcmcs["name"]}.mle.log">\n'
            mcmc += f'{tab3}<pathLikelihood idref="pathLikelihood"/>\n'
            mcmc += f'{tab2}</log>\n'
            mcmc += f'{tab1}</marginalLikelihoodEstimator>\n'
            mcmc += f'{tab1}<!-- Path sampling estimator from collected samples -->\n'
            mcmc += f'{tab1}<pathSamplingAnalysis fileName="{self.mcmcs["name"]}.mle.log">\n'
            mcmc += f'{tab2}<likelihoodColumn name="pathLikelihood.delta"/>\n'
            mcmc += f'{tab2}<thetaColumn name="pathLikelihood.theta"/>\n'
            mcmc += f'{tab1}</pathSamplingAnalysis>\n'
            mcmc += f'{tab1}<!-- Stepping-stone sampling estimator from collected samples -->\n'
            mcmc += f'{tab1}<steppingStoneSamplingAnalysis fileName="{self.mcmcs["name"]}.mle.log">\n'
            mcmc += f'{tab2}<likelihoodColumn name="pathLikelihood.delta"/>\n'
            mcmc += f'{tab2}<thetaColumn name="pathLikelihood.theta"/>\n'
            mcmc += f'{tab1}</steppingStoneSamplingAnalysis>\n'
            
        return mcmc
                
