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
        xml += self._get_general_datatype(self.datatype)
        xml += self._add_comment("ALIGNMENT")
        xml += self.fasta.get_fasta_alignment(self.datatype)
        xml += self._add_comment("CHARACTER PATTERNS")
        xml += self._get_character_patterns(self.datatype)
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
        xml += self._get_frequency_model(self.datatype)
        xml += self._add_comment("CNA MODEL")
        xml += self._get_cna_model(self.datatype)
        xml += self._add_comment("SITE MODEL")
        xml += self._get_site_model(self.datatype)                
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
        
    
    ### PRIVATE HELPERS #########
    def _get_general_datatype(self,datatype):
        gdt = ""
        if datatype == "acna":        
            gdt += "<generalDataType id=\"acna\">" + "\n"
            gdt += "\t<state code=\"@\"/> <!-- Genotype: 0 ; Beast State: 0 -->" + "\n"
            gdt += "\t<state code=\"A\"/> <!-- Genotype: 1 ; Beast State: 1 -->" + "\n"
            gdt += "\t<state code=\"B\"/> <!-- Genotype: 2 ; Beast State: 2 -->" + "\n"
            gdt += "\t<state code=\"C\"/> <!-- Genotype: 3 ; Beast State: 3 -->" + "\n"
            gdt += "\t<state code=\"D\"/> <!-- Genotype: 4 ; Beast State: 4 -->" + "\n"
            gdt += "\t<state code=\"E\"/> <!-- Genotype: 5 ; Beast State: 5 -->" + "\n"
            gdt += "\t<state code=\"F\"/> <!-- Genotype: 6 ; Beast State: 6 -->" + "\n"
            gdt += "\t<state code=\"G\"/> <!-- Genotype: 7 ; Beast State: 7 -->" + "\n"
            gdt += "\t<state code=\"H\"/> <!-- Genotype: 8 ; Beast State: 8 -->" + "\n"
            gdt += "\t<state code=\"I\"/> <!-- Genotype: 9 ; Beast State: 9 -->" + "\n"
            gdt += "\t<state code=\"J\"/> <!-- Genotype: 10 ; Beast State: 10 -->" + "\n"
            gdt += "\t<ambiguity code=\"-\" states=\"@ABCDEFGHIJ\"/>" + "\n"
            gdt += "\t<ambiguity code=\"?\" states=\"@ABCDEFGHIJ\"/>" + "\n"
            gdt += "</generalDataType>" + "\n"
        elif datatype == "cnv":
            gdt += '\t<generalDataType id="cnv">\n'
            gdt += '\t<state code="@"/> <!-- Genotype: 0,0 ; Beast State: 0 -->\n'
            gdt += '\t<state code="A"/> <!-- Genotype: 0,1 ; Beast State: 1 -->\n'
            gdt += '\t<state code="B"/> <!-- Genotype: 0,2 ; Beast State: 2 -->\n'
            gdt += '\t<state code="C"/> <!-- Genotype: 0,3 ; Beast State: 3 -->\n'
            gdt += '\t<state code="D"/> <!-- Genotype: 0,4 ; Beast State: 4 -->\n'
            gdt += '\t<state code="E"/> <!-- Genotype: 0,5 ; Beast State: 5 -->\n'
            gdt += '\t<state code="F"/> <!-- Genotype: 0,6 ; Beast State: 6 -->\n'
            gdt += '\t<state code="G"/> <!-- Genotype: 1,0 ; Beast State: 7 -->\n'
            gdt += '\t<state code="H"/> <!-- Genotype: 1,1 ; Beast State: 8 -->\n'
            gdt += '\t<state code="I"/> <!-- Genotype: 1,2 ; Beast State: 9 -->\n'
            gdt += '\t<state code="J"/> <!-- Genotype: 1,3 ; Beast State: 10 -->\n'
            gdt += '\t<state code="K"/> <!-- Genotype: 1,4 ; Beast State: 11 -->\n'
            gdt += '\t<state code="L"/> <!-- Genotype: 1,5 ; Beast State: 12 -->\n'
            gdt += '\t<state code="M"/> <!-- Genotype: 2,0 ; Beast State: 13 -->\n'
            gdt += '\t<state code="N"/> <!-- Genotype: 2,1 ; Beast State: 14 -->\n'
            gdt += '\t<state code="O"/> <!-- Genotype: 2,2 ; Beast State: 15 -->\n'
            gdt += '\t<state code="P"/> <!-- Genotype: 2,3 ; Beast State: 16 -->\n'
            gdt += '\t<state code="Q"/> <!-- Genotype: 2,4 ; Beast State: 17 -->\n'
            gdt += '\t<state code="R"/> <!-- Genotype: 3,0 ; Beast State: 18 -->\n'
            gdt += '\t<state code="S"/> <!-- Genotype: 3,1 ; Beast State: 19 -->\n'
            gdt += '\t<state code="T"/> <!-- Genotype: 3,2 ; Beast State: 20 -->\n'
            gdt += '\t<state code="U"/> <!-- Genotype: 3,3 ; Beast State: 21 -->\n'
            gdt += '\t<state code="V"/> <!-- Genotype: 4,0 ; Beast State: 22 -->\n'
            gdt += '\t<state code="W"/> <!-- Genotype: 4,1 ; Beast State: 23 -->\n'
            gdt += '\t<state code="X"/> <!-- Genotype: 4,2 ; Beast State: 24 -->\n'
            gdt += '\t<state code="Y"/> <!-- Genotype: 5,0 ; Beast State: 25 -->\n'
            gdt += '\t<state code="Z"/> <!-- Genotype: 5,1 ; Beast State: 26 -->\n'
            gdt += '\t<state code="["/> <!-- Genotype: 6,0 ; Beast State: 27 -->\n'
            gdt += '\t<ambiguity code="-" states="@ABCDEFGHIJKLMNOPQRSTUVWXYZ["/>\n'
            gdt += '\t<ambiguity code="?" states="@ABCDEFGHIJKLMNOPQRSTUVWXYZ["/>\n'
            gdt += '\t</generalDataType>\n'
        elif datatype == "bb" or datatype == "biallelicBinary":
            gdt += '<generalDataType id="biallelicBinary">\n'
            gdt += '<state code="0"/> <!-- Genotype: 0 ; Beast State: 0 -->\n'
            gdt += '<state code="1"/> <!-- Genotype: 1 ; Beast State: 1 -->\n'
            gdt += '<state code="2"/> <!-- Genotype: 2 ; Beast State: 2 -->\n'
            gdt += '</generalDataType>\n' 
        return gdt
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
    def _get_character_patterns(self,datatype):
        pat = ""
        if datatype == "bb" or datatype == "biallelicBinary":
            pat += '<patterns id="patterns" from="1">\n'
            pat += '\t<alignment idref="alignment"/>\n'
            pat += '</patterns>\n'
        else:
            state = "H"
            if datatype == "acna":
                state = "B"            
            pat += '<ascertainedCharacterPatterns id="patterns">\n'
            pat += '\t<alignment idref="alignment"/>\n'
            pat += f'\t<state code="{state}"/>\n'
            pat += '</ascertainedCharacterPatterns>\n'
        return pat
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
    def _get_frequency_model(self,datatype):
        if datatype == "bb":
            datatype = "biallelicBinary"
        fm = ""        
        fm += '<frequencyModel id="frequencies">\n'
        fm += f'\t<dataType idref="{datatype}"/>\n'
        fm += '\t<frequencies>\n'
        if datatype == "acna":
            fm += f'\t\t<parameter id="{datatype}.frequencies" value="0 0 1 0 0 0 0 0 0 0 0"/>\n'
        elif datatype == "cnv":
            fm += f'\t\t<parameter id="{datatype}.frequencies" value="0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0"/>\n'
        elif datatype == "biallelicBinary":
            fm += f'\t\t<parameter id="{datatype}.frequencies" value="0.5 0 0.5"/>\n'
        fm += '\t</frequencies>\n'
        fm += '</frequencyModel>\n'	   	  
        return fm
    #----------------------------------
    def _get_cna_model(self,datatype):
        cna = ""
        if datatype == "acna":            
            cna += '<AbsoluteCNAModel id="acna_subsmodel">\n'
            cna += '\t<frequencies>\n'
            cna += '\t\t<frequencyModel idref="frequencies"/>\n'
            cna += '\t</frequencies>\n'
            cna += '\t<gain_rate>\n'
            cna += '\t\t<parameter id="acna.gain" value="1" lower="0"/>\n'
            cna += '\t</gain_rate>\n'
            cna += '\t<relative_loss_rate>\n'
            cna += '\t\t<parameter id="acna.loss" value="1" lower="0"/>\n'
            cna += '\t</relative_loss_rate>\n'
            cna += '</AbsoluteCNAModel>\n'
        elif datatype == "cnv":
            cna += '<CNVModel id="cnv_subsmodel">\n'
            cna += '\t<frequencies>\n'
            cna += '\t\t<frequencyModel idref="frequencies"/>\n'
            cna += '\t</frequencies>\n'
            cna += '\t<gain_rate>\n'
            cna += '\t\t<parameter id="cnv.gain" value="1" lower="0"/>\n'
            cna += '\t</gain_rate>\n'
            cna += '\t<loss_rate>\n'
            cna += '\t\t<parameter id="cnv.loss" value="1" lower="0"/>\n'
            cna += '\t</loss_rate>\n'
            cna += '\t<conversion_rate>\n'
            cna += '\t\t<parameter id="cnv.conversion" value="1" lower="0"/>\n'
            cna += '\t</conversion_rate>\n'
            cna += '</CNVModel>\n'            
        elif datatype == "bb" or datatype == "biallelicBinary":
            cna += '<BiallelicBinaryModel id="biallelicBinary_subsmodel">\n'
            cna += '\t<frequencies>\n'
            cna += '\t\t<frequencyModel idref="frequencies"/>\n'
            cna += '\t</frequencies>\n'                        
            cna += '\t<demethylation_rate>\n'
            cna += '\t\t<parameter id="biallelicBinary.demethylation" value="1" lower="0"/>\n'
            cna += '\t</demethylation_rate>\n'
            cna += '\t<homozygousDemethylation_rate>\n'
            cna += '\t\t<parameter id="biallelicBinary.homozygousDemethylation" value="1" lower="0"/>\n'
            cna += '\t</homozygousDemethylation_rate>\n'
            cna += '\t<homozygousMethylation_rate>\n'
            cna += '\t\t<parameter id="biallelicBinary.homozygousMethylation" value="1" lower="0"/>\n'
            cna += '\t</homozygousMethylation_rate>\n'                    
            cna += '</BiallelicBinaryModel>\n'            
        return cna
    #----------------------------------
    def _get_site_model(self,datatype):
        st = ""
        if datatype == "acna":
            st += '<siteModel id="siteModel">\n'
            st += '\t<substitutionModel>\n'
            st += '\t\t<AbsoluteCNAModel idref="acna_subsmodel"/>\n'
            st += '\t</substitutionModel>\n'
            st += '</siteModel>\n'
        elif datatype == "cnv":
            st += '<siteModel id="siteModel">\n'
            st += '\t<substitutionModel>\n'
            st += '\t\t<CNVModel idref="cnv_subsmodel"/>\n'
            st += '\t</substitutionModel>\n'
            st += '</siteModel>\n'            
        elif datatype == "bb" or datatype == "biallelicBinary":
            st += '<siteModel id="siteModel">\n'
            st += '\t<substitutionModel>\n'
            st += '\t\t<BiallelicBinaryModel idref="biallelicBinary_subsmodel"/>\n'
            st += '\t</substitutionModel>\n'
            st += '</siteModel>\n'            
        return st
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
    
