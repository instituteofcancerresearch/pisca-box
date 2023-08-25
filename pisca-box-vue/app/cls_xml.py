
class XmlWriter(object):
    def __init__(self,fasta,mcmc,lucas,clock):        
        self.fasta = fasta
        self.mcmc = mcmc
        self.lucas = lucas
        self.clock = clock
        
    ### PUBLIC INTERFACE #########
    def get_xml(self):
        xml = ""
        xml += self._get_xml_header()
        xml += self.fasta.get_fasta_taxa()        
        xml += self._get_general_datatype()
        xml += self.fasta.get_fasta_alignment()
        xml += self._get_character_patterns()
        xml += self._get_constant_size()
        xml += self._get_coalescent_simulator()
        xml += self._get_tree_model()
        xml += self._get_coalescent_likelihood()
        xml += self._get_cenancestor_clock(self.clock)
        xml += self._get_sum_statistic()
        xml += self._get_rates()
        xml += self._get_frequency_model()
        xml += self._get_cnv_model()
        xml += self._get_site_model()        
        lh_val,lh_up,lh_low,lb_val,lb_up,lb_low = self.lucas
        xml += self._get_tree_likelihood(lh_val,lh_up,lh_low,lb_val,lb_up,lb_low)
        xml += self._get_operators()
        xml += self.mcmc.get_mcmc()
        xml += self._get_report()
        xml += self._get_xml_footer()
        return xml
        
    
    ### PRIVATE HELPERS #########
    def _get_general_datatype(self):
        gdt = ""
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
    def _get_character_patterns(self):
        pat = ""
        pat += '<ascertainedCharacterPatterns id="patterns">\n'
        pat += '\t<alignment idref="alignment"/>\n'
        pat += '\t<state code="H"/>\n'
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
    def _get_coalescent_simulator(self):
        cs = ""
        cs += '<coalescentSimulator id="startingTree">\n'
        cs += '\t<taxa idref="taxa"/>\n'
        cs += '\t<constantSize idref="constant"/>\n'
        cs += '</coalescentSimulator>\n'
        return cs
    #----------------------------------
    def _get_tree_model(self):
        return ""
    #----------------------------------
    def _get_coalescent_likelihood(self):
        return ""
    #----------------------------------
    def _get_cenancestor_clock(self,clock):
        if clock == "strict clock":
            return self._get_strict_clock()
        else:
            return self._get_random_clock()                    
    #----------------------------------
    def _get_strict_clock(self):
        cl = ""
        cl += f'<strictClockCenancestorBranchRates id="branchRates">\n'
        cl += f'\t<rate>\n'
        cl += f'\t\t<parameter id="clock.rate" value="1"/>\n'
        cl += f'\t</rate>\n'
        cl += f'</strictClockCenancestorBranchRates>\n'
        return cl            
    #----------------------------------    
    def _get_random_clock(self):
        cl = ""
        cl += f'<randomLocalClockModelCenancestor id="branchRates" ratesAreMultipliers="false">\n'
        cl += f'\t<treeModel idref="treeModel"/>\n'
        cl += f'\t<rates>\n'
        cl += f'\t\t<parameter id="localClock.relativeRates"/>\n'
        cl += f'\t</rates>\n'
        cl += f'\t<rateIndicator>\n'
        cl += f'\t\t<parameter id="localClock.changes"/>\n'
        cl += f'\t</rateIndicator>\n'
        cl += f'\t<clockRate>\n'
        cl += f'\t\t<parameter id="clock.rate" value="1.0" lower="0.0"/>\n'
        cl += f'\t</clockRate>\n'
        cl += f'</randomLocalClockModelCenancestor>\n'
        return cl   
    #----------------------------------
    def _get_sum_statistic(self):
        return ""
    #----------------------------------
    def _get_rates(self):
        return ""
    #----------------------------------
    def _get_frequency_model(self):
        return ""
    #----------------------------------
    def _get_cnv_model(self):
        return ""
    #----------------------------------
    def _get_site_model(self):
        return ""
    #----------------------------------
    def _get_tree_likelihood(self,lh_val,lh_up,lh_low,lb_val,lb_up,lb_low):        
        cen = ""
        cen += f'<cenancestorTreeLikelihood id="treeLikelihood" useAmbiguities="false">\n'
        cen += f'\t<patterns idref="patterns"/>\n'
        cen += f'\t<treeModel idref="treeModel"/>\n'
        cen += f'\t<siteModel idref="siteModel"/>\n'
        cen += f'\t<cenancestorHeight>\n'
        cen += f'\t\t<parameter id="luca_height" value="{lh_val}" upper="{lh_up}" lower="{lh_low}"/>\n'
        cen += f'\t</cenancestorHeight>\n'
        cen += f'\t<cenancestorBranch>\n'
        cen += f'\t\t<parameter id="luca_branch" value="{lb_val}" upper="{lb_up}" lower="{lb_low}"/>\n'
        cen += f'\t</cenancestorBranch>\n'
        cen += f'\t<randomLocalClockModelCenancestor idref="branchRates"/>\n'
        cen += f'</cenancestorTreeLikelihood>\n'
        return cen
    #----------------------------------
    def _get_operators(self):
        return ""
    #----------------------------------        
    def _get_report(self):
        return ""
    #----------------------------------
    
