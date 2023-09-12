


class MCMC(object):
    def __init__(self, name, chain_length, log_every,clock):
        self.name = name
        self.chain_length = chain_length
        self.log_every = log_every
        self.clock = clock
        
        
    ### PUBLIC INTERFACE ######### 
    def get_mcmc(self,datatype,demographic):
        tab1 = ""
        tab2 = "\t"
        tab3 = "\t\t"
        tab4 = "\t\t\t"
        tab5 = "\t\t\t\t"
        mcmc = ""                             
        mcmc += f'{tab1}<mcmc id="mcmc" chainLength="{self.chain_length}" autoOptimize="true" operatorAnalysis="{self.name}.ops">\n'
        mcmc += f'{tab2}<posterior id="posterior">\n'
        mcmc += f'{tab3}<prior id="prior">\n'
        mcmc += f'{tab4}<coalescentLikelihood idref="coalescent"/>\n'
        if demographic == "constant size":
            mcmc += f'{tab4}<oneOnXPrior>\n'
            mcmc += f'{tab5}<parameter idref="constant.popSize"/>\n'
            mcmc += f'{tab4}</oneOnXPrior>\n'            
        elif demographic == "exponential growth":        
            mcmc += f'{tab4}<oneOnXPrior>\n'
            mcmc += f'{tab5}<parameter idref="exponential.popSize"/>\n'
            mcmc += f'{tab4}</oneOnXPrior>\n'
            mcmc += f'{tab4}<laplacePrior mean="0.0" scale="1.0">\n'
            mcmc += f'{tab5}<parameter idref="exponential.growthRate"/>\n'
            mcmc += f'{tab4}</laplacePrior>\n'

        mcmc += f'{tab4}<!-- Clock (gain) Rate Prior. -->\n'
        mcmc += f'{tab4}<logNormalPrior mean="0.1" stdev="3" offset="0.0" meanInRealSpace="true">\n'
        mcmc += f'{tab5}<parameter idref="clock.rate"/>\n'
        mcmc += f'{tab4}</logNormalPrior>\n'

        mcmc += f'{tab4}<!-- Loss (relative to gain) rate priors-->\n'
        mcmc += f'{tab4}<exponentialPrior mean="1.0" offset="0.0">\n'
        mcmc += f'{tab5}<parameter idref="{datatype}.loss"/>\n'
        mcmc += f'{tab4}</exponentialPrior>\n'

        mcmc += f'{tab4}<!-- Cenancestor Prior on the height, since it is easier to have a meaningfull prior on it (time of the initial development of the BE fragment) -->\n'
        mcmc += f'{tab4}<uniformPrior lower="1" upper="50">\n'
        mcmc += f'{tab5}<parameter idref="luca_height"/>\n'
        mcmc += f'{tab4}</uniformPrior>\n'
        mcmc += f'{tab3}</prior>\n'

        mcmc += f'{tab3}<likelihood id="likelihood">\n'
        mcmc += f'{tab4}<cenancestorTreeLikelihood idref="treeLikelihood"/>\n'
        mcmc += f'{tab3}</likelihood>\n'
        mcmc += f'{tab2}</posterior>\n'
        mcmc += f'{tab2}<operators idref="operators"/>\n'

        mcmc += f'{tab2}<!-- write log to screen -->\n'
        mcmc += f'{tab2}<log id="screenLog" logEvery="{self.log_every}">\n'
        mcmc += f'{tab3}<column label="Posterior" dp="4" width="12">\n'
        mcmc += f'{tab4}<posterior idref="posterior"/>\n'
        mcmc += f'{tab3}</column>\n'
        mcmc += f'{tab3}<column label="Prior" dp="4" width="12">\n'
        mcmc += f'{tab4}<prior idref="prior"/>\n'
        mcmc += f'{tab3}</column>\n'
        mcmc += f'{tab3}<column label="Likelihood" dp="4" width="12">\n'
        mcmc += f'{tab4}<likelihood idref="likelihood"/>\n'
        mcmc += f'{tab3}</column>\n'
        mcmc += f'{tab3}<column label="rel_loss_rate" sf="6" width="12">\n'
        mcmc += f'{tab4}<parameter idref="{datatype}.loss"/>\n'
        mcmc += f'{tab3}</column>\n'
        mcmc += f'{tab3}<column label="clock_rate" sf="6" width="12">\n'
        mcmc += f'{tab4}<parameter idref="clock.rate"/>\n'
        mcmc += f'{tab3}</column>\n'
        mcmc += f'{tab3}<column label="rootHeight" sf="6" width="12">\n'
        mcmc += f'{tab4}<parameter idref="treeModel.rootHeight"/>\n'
        mcmc += f'{tab3}</column>\n'
        mcmc += f'{tab3}<column label="luca_height" sf="6" width="12">\n'
        mcmc += f'{tab4}<parameter idref="luca_height"/>\n'
        mcmc += f'{tab3}</column>\n'
        mcmc += f'{tab3}<column label="luca_branch" sf="6" width="12">\n'
        mcmc += f'{tab4}<parameter idref="luca_branch"/>\n'
        mcmc += f'{tab3}</column>\n'
        mcmc += f'{tab2}</log>\n'

        mcmc += f'{tab2}<!-- write log to file  -->\n'
        mcmc += f'{tab2}<log id="fileLog" logEvery="{self.log_every}" fileName="{self.name}.log" overwrite="false">\n'
        mcmc += f'{tab3}<posterior idref="posterior"/>\n'
        mcmc += f'{tab3}<prior idref="prior"/>\n'
        mcmc += f'{tab3}<likelihood idref="likelihood"/>\n'
        mcmc += f'{tab3}<parameter idref="{datatype}.loss"/>\n'
        mcmc += f'{tab3}<parameter idref="treeModel.rootHeight"/>\n'
        mcmc += f'{tab3}<parameter idref="luca_height"/>\n'
        mcmc += f'{tab3}<parameter idref="luca_branch"/>\n'                
        mcmc += f'{tab3}<parameter idref="clock.rate"/>\n'
        mcmc += f'{tab3}<coalescentLikelihood idref="coalescent"/>\n'        
        if demographic == "exponential growth":
            mcmc += f'{tab3}<parameter idref="exponential.popSize"/>\n'
            mcmc += f'{tab3}<parameter idref="exponential.growthRate"/>\n'
        elif demographic == "constant size":
            mcmc += f'{tab3}<parameter idref="constant.popSize"/>\n'
        if self.clock == "random local clock":            
            mcmc += f'{tab3}<parameter idref="localClock.relativeRates"/>\n'
            mcmc += f'{tab3}<parameter idref="localClock.changes"/>\n'
            mcmc += f'{tab3}<statistic idref="rateChanges"/>\n'
            mcmc += f'{tab3}<rateStatisticCenancestor idref="coefficientOfVariation"/>\n'
            mcmc += f'{tab3}<rateCovarianceStatistic idref="covariance"/>\n'
            mcmc += f'{tab3}<rateStatisticCenancestor idref="cenancestorRate"/>\n'
        
            
        mcmc += f'{tab2}</log>\n'

        mcmc += f'{tab2}<!-- write tree log to file   -->\n'
        mcmc += f'{tab2}<logTree id="treeFileLog" logEvery="{self.log_every}" nexusFormat="true" fileName="{self.name}.trees" sortTranslationTable="true">\n'
        mcmc += f'{tab3}<treeModel idref="treeModel"/>\n'        
        if self.clock == "random local clock":
            mcmc += f'{tab3}<trait name="rate" tag="rate">\n'
            mcmc += f'{tab4}<randomLocalClockModelCenancestor idref="branchRates"/>\n'
            mcmc += f'{tab3}</trait>\n'
            mcmc += f'{tab3}<trait name="rates" tag="relRates">\n'        
            mcmc += f'{tab4}<randomLocalClockModelCenancestor idref="branchRates"/>\n'
            mcmc += f'{tab3}</trait>\n'
            mcmc += f'{tab3}<trait name="rateIndicator" tag="indicator">\n'
            mcmc += f'{tab4}<randomLocalClockModelCenancestor idref="branchRates"/>\n'
            mcmc += f'{tab3}</trait>\n'
        elif self.clock == "strict clock":
            mcmc += f'{tab3}<trait name="rate" tag="rate">\n'
            mcmc += f'{tab4}<strictClockCenancestorBranchRates idref="branchRates"/>\n'
            mcmc += f'{tab3}</trait>\n'
        mcmc += f'{tab3}<posterior idref="posterior"/>\n'
        mcmc += f'{tab2}</logTree>\n'
        mcmc += f'{tab1}</mcmc>\n'                        
        return mcmc
    
    
