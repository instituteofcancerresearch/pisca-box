# ruff: noqa: E501

class XmlWriter(object):
    def __init__(self,fasta,mcmc,lucas,clocks,demographic,datatype,operators):        
        self.fasta = fasta
        self.mcmc = mcmc
        self.lucas = lucas
        self.clocks = clocks
        self.demographic = demographic
        self.datatype = datatype
        self.operators = operators
        
    ### PUBLIC INTERFACE #########
    def get_xml(self):
        xml = ""
        xml += self._get_xml_header()
        xml += self._add_comment("TAXA")
        xml += self.fasta.get_fasta_taxa()        
        xml += self._add_comment("GENERAL DATATYPE")
        xml += self.fasta.get_datatype_xml()
        xml += self._add_comment("ALIGNMENT")
        xml += self.fasta.get_fasta_alignment()
        xml += self._add_comment("CHARACTER PATTERNS")
        xml += self.fasta.get_character_patterns()
        if self.demographic == "constant size":
            xml += self._add_comment("CONSTANT SIZE")
            xml += self._get_constant_size()
            xml += self._get_coalescent_simulator("constant")            
            xml += self._add_comment("TREE MODEL")
            xml += self._get_tree_model()
            xml += self._get_coalescent_likelihood("constant")
        elif self.demographic == "exponential growth":
            xml += self._add_comment("EXPONENTIAL GROWTH")
            xml += self._get_exponential_growth("assumption that pop size remained EXPO over time spanned by the geneology")
            xml += self._get_coalescent_simulator("exponential")            
            xml += self._add_comment("TREE MODEL")
            xml += self._get_tree_model()
            xml += self._get_coalescent_likelihood("exponential")                                    
        xml += self._add_comment("CENANCESTOR CLOCK")
        xml += self._get_cenancestor_clock(self.clocks)
        if self.clocks['type'] == "random local clock":
            xml += self._get_sum_statistic()
            xml += self._get_rates()        
        xml += self._add_comment("FREQUENCY MODEL")
        xml += self.fasta.get_frequency_model()
        xml += self._add_comment("CNA MODEL")
        xml += self.fasta.get_cna_model()
        xml += self._add_comment("SITE MODEL")
        xml += self.fasta.get_site_model()
        lh_val,lb_val,lb_up,lb_low = self.lucas["height"],self.lucas["branch"],self.lucas["upper"],self.lucas["lower"]
        xml += self._add_comment("TREE LIKELIHOOD")
        xml += self._get_tree_likelihood(lh_val,lb_val,lb_up,lb_low, self.clocks)
        xml += self._add_comment("OPERATORS")
        xml += self.operators.get_operators()
        xml += self._add_comment("MCMC and PRIORS")
        xml += self.mcmc.get_mcmc(self.datatype,self.demographic)
        xml += self._add_comment("REPORT")
        xml += self._get_report()
        xml += self._get_xml_footer()
        return xml                
    #----------------------------------
    def _get_xml_header(self):
        hdr = ""
        hdr += '<?xml version="1.0" standalone="yes"?>' + "\n"
        hdr += "<beast>" + "\n"        
        return hdr
    #----------------------------------
    def _get_xml_footer(self):
        ftr = ""
        ftr += "</beast>"        
        return ftr    
    #----------------------------------
    def _get_constant_size(self):
        cs = ""        
        cs += '<constantSize id="constant" units="years">\n'
        cs += '\t<populationSize>\n'
        cs += '\t\t<parameter id="constant.popSize" value="1" lower="0.0"/>\n'
        cs += '\t</populationSize>\n'
        cs += '</constantSize>\n'             
        return cs
    #----------------------------------
    def _get_exponential_growth(self, comment):
        eg = f"<!-- {comment} -->\n"
        eg += '<exponentialGrowth id="exponential" units="years">\n'
        eg += '\t<populationSize>\n'
        eg += '\t\t<parameter id="exponential.popSize" value="1" lower="0.0"/>\n'
        eg += '\t</populationSize>\n'
        eg += '\t<growthRate>\n'
        eg += '\t\t<parameter id="exponential.growthRate" value="1.0"/>\n'
        eg += '\t</growthRate>\n'
        eg += '</exponentialGrowth>\n'
        return eg
    #----------------------------------
    def _get_coalescent_simulator(self,demographic):
        cs = ""
        cs += '<coalescentSimulator id="startingTree">\n'
        cs += '\t<taxa idref="taxa"/>\n'
        if demographic == "constant":
            cs += '\t<constantSize idref="constant"/>\n'
        elif demographic == "exponential":
            cs += '\t<exponentialGrowth idref="exponential"/>\n'
        cs += '</coalescentSimulator>\n'
        return cs
    #----------------------------------
    def _get_tree_model(self):
        tm = ""
        tm += '<treeModel id="treeModel">\n'
        tm += '\t<coalescentTree idref="startingTree"/>\n'
        tm += '\t<rootHeight>\n'
        tm += '\t\t<parameter id="treeModel.rootHeight"/>\n'
        tm += '\t</rootHeight>\n'
        tm += '\t<nodeHeights internalNodes="true">\n'
        tm += '\t\t<parameter id="treeModel.internalNodeHeights"/>\n'
        tm += '\t</nodeHeights>\n'
        tm += '\t<nodeHeights internalNodes="true" rootNode="true">\n'
        tm += '\t\t<parameter id="treeModel.allInternalNodeHeights"/>\n'
        tm += '\t</nodeHeights>\n'
        tm += '</treeModel>\n'
        return tm
    #----------------------------------
    def _get_coalescent_likelihood(self,demographic):
        cl = ""
        cl += '<coalescentLikelihood id="coalescent">\n'
        cl += '\t<model>\n'
        if demographic == "constant":
            cl += '\t\t<constantSize idref="constant"/>\n'                  
        elif demographic == "exponential":
            cl += '\t\t<exponentialGrowth idref="exponential"/>\n'                    
        cl += '\t</model>\n'
        cl += '\t<populationTree>\n'
        cl += '\t\t<treeModel idref="treeModel"/>\n'
        cl += '\t</populationTree>\n'
        cl += '</coalescentLikelihood>\n'
        return cl
    #----------------------------------
    def _get_cenancestor_clock(self,clocks):
        if clocks['type'] == "strict clock":
            return self._get_strict_clock()
        else:
            return self._get_random_clock()                    
    #----------------------------------
    def _get_strict_clock(self):
        rate = self.clocks['rate']
        cl = ""
        cl += '<strictClockCenancestorBranchRates id="branchRates">\n'
        cl += '\t<rate>\n'
        cl += f'\t\t<parameter id="clock.rate" value="{rate}"/>\n'
        cl += '\t</rate>\n'
        cl += '</strictClockCenancestorBranchRates>\n'
        return cl            
    #----------------------------------    
    def _get_random_clock(self):
        cl = ""
        cl += '<randomLocalClockModelCenancestor id="branchRates" ratesAreMultipliers="false">\n'
        cl += '\t<treeModel idref="treeModel"/>\n'
        cl += '\t<rates>\n'
        cl += '\t\t<parameter id="localClock.relativeRates"/>\n'
        cl += '\t</rates>\n'
        cl += '\t<rateIndicator>\n'
        cl += '\t\t<parameter id="localClock.changes"/>\n'
        cl += '\t</rateIndicator>\n'
        cl += '\t<clockRate>\n'
        cl += '\t\t<parameter id="clock.rate" value="1.0" lower="0.0"/>\n'
        cl += '\t</clockRate>\n'
        cl += '</randomLocalClockModelCenancestor>\n'
        return cl   
    #----------------------------------
    def _get_sum_statistic(self):
        ss = ""
        ss += '<sumStatistic id="rateChanges" name="rateChangeCount" elementwise="true">\n'
        ss += '\t<parameter idref="localClock.changes"/>\n'
        ss += '</sumStatistic>\n'
        return ss
    #----------------------------------
    def _get_rates(self):
        rts = ""
        rts += '<rateStatisticCenancestor id="cenancestorRate" name="cenancestorRate" mode="cenancestor" internal="true" external="true">\n'
        rts += '\t<treeModel idref="treeModel"/>\n'
        rts += '\t<randomLocalClockModelCenancestor idref="branchRates"/>\n'
        rts += '</rateStatisticCenancestor>\n'
        rts += '<rateStatisticCenancestor id="coefficientOfVariation" name="coefficientOfVariation" mode="coefficientOfVariation" internal="true" external="true">\n'
        rts += '\t<treeModel idref="treeModel"/>\n'
        rts += '\t<randomLocalClockModelCenancestor idref="branchRates"/>\n'
        rts += '</rateStatisticCenancestor>\n'
        rts += '<rateCovarianceStatistic id="covariance" name="covariance">\n'
        rts += '\t<treeModel idref="treeModel"/>\n'
        rts += '\t<randomLocalClockModelCenancestor idref="branchRates"/>\n'
        rts += '</rateCovarianceStatistic>\n'
        return rts                
    #----------------------------------
    def _get_tree_likelihood(self,lh_val,lb_val,lb_up,lb_low,clocks):        
        cen = ""
        cen += '<cenancestorTreeLikelihood id="treeLikelihood" useAmbiguities="false">\n'
        cen += '\t<patterns idref="patterns"/>\n'
        cen += '\t<treeModel idref="treeModel"/>\n'
        cen += '\t<siteModel idref="siteModel"/>\n'
        cen += '\t<cenancestorHeight>\n'
        cen += f'\t\t<parameter id="luca_height" value="{lh_val}"/>\n'
        cen += '\t</cenancestorHeight>\n'
        cen += '\t<cenancestorBranch>\n'
        cen += f'\t\t<parameter id="luca_branch" value="{lb_val}" upper="{lb_up}" lower="{lb_low}"/>\n'
        cen += '\t</cenancestorBranch>\n'
        if clocks['type'] == "strict clock":
            cen += '\t<strictClockCenancestorBranchRates idref="branchRates"/>\n'
        elif clocks['type'] == "random local clock":
            cen += '\t<randomLocalClockModelCenancestor idref="branchRates"/>\n'
        cen += '</cenancestorTreeLikelihood>\n'
        return cen        
    #----------------------------------        
    def _get_report(self):
        rp = ""
        rp += '<report>\n'
        rp += '\t<property name="timer">\n'
        rp += '\t\t<mcmc idref="mcmc"/>\n'
        rp += '\t</property>\n'
        rp += '</report>\n'
        return rp
    
    def _add_comment(self,comment):
        return f"<!-- {comment} -->\n"        
    #----------------------------------
    
