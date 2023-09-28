
# ruff: noqa: E501

class Operators(object):
    def __init__(self,datatype,ops):
        self.datatype = datatype
        self.ops = ops
                        
    ### PUBLIC INTERFACE #########    
    #----------------------------------
    def get_operators(self, demographic,datatype,clocks):
        if datatype == "bb":
            datatype = "biallelicBinary"
        op = ""
        op += '<operators id="operators" optimizationSchedule="default">\n'
        if datatype != "biallelicBinary":
            op += '\t<scaleOperator scaleFactor="0.25" weight="0.25">\n'
            op += f'\t\t<parameter idref="{datatype}.loss"/>\n'
            op += '\t</scaleOperator>\n'        
        op += '\t<scaleOperator scaleFactor="0.5" weight="10.0">\n'
        op += '\t\t<parameter idref="clock.rate"/>\n'
        op += '\t</scaleOperator>\n'                
        if clocks['type'] == "random local clock":
            op += '\t<scaleOperator scaleFactor="0.75" weight="15">\n'
            op += '\t\t<parameter idref="localClock.relativeRates"/>\n'
            op += '\t</scaleOperator>\n'        
            op += '\t<bitFlipOperator weight="15">\n'
            op += '\t\t<parameter idref="localClock.changes"/>\n'
            op += '\t</bitFlipOperator>\n'        
        op += '\t<subtreeSlide size="2.5" gaussian="true" weight="15.0"> <!-- 2.5 years. They will be automatically optimized by BEAST though -->\n'
        op += '\t\t<treeModel idref="treeModel"/>\n'
        op += '\t</subtreeSlide>\n'        
        op += '\t<narrowExchange weight="15.0">\n'
        op += '\t\t<treeModel idref="treeModel"/>\n'
        op += '\t</narrowExchange>\n'        
        op += '\t<wideExchange weight="3.0">\n'
        op += '\t\t<treeModel idref="treeModel"/>\n'
        op += '\t</wideExchange>\n'        
        op += '\t<wilsonBalding weight="3.0">\n'
        op += '\t\t<treeModel idref="treeModel"/>\n'
        op += '\t</wilsonBalding>\n'        
        op += '\t<scaleOperator scaleFactor="0.75" weight="5.0">\n'
        op += '\t\t<parameter idref="treeModel.rootHeight"/>\n'
        op += '\t</scaleOperator>\n'        
        op += '\t<uniformOperator weight="30.0">\n'
        op += '\t\t<parameter idref="treeModel.internalNodeHeights"/>\n'
        op += '\t</uniformOperator>\n'        
        op += '\t<scaleOperator scaleFactor="0.2" weight="1.0">\n'
        op += '\t\t<parameter idref="luca_branch"/>\n'
        op += '\t</scaleOperator>\n'        
        if demographic == "constant size":
            op += '\t<scaleOperator scaleFactor="0.5" weight="3.0">\n'
            op += '\t\t<parameter idref="constant.popSize"/>\n'
            op += '\t</scaleOperator>\n'
        elif demographic == "exponential growth":
            op += '\t<scaleOperator scaleFactor="0.5" weight="3.0">\n'
            op += '\t\t<parameter idref="exponential.popSize"/>\n'
            op += '\t</scaleOperator>\n'
            op += '\t<randomWalkOperator windowSize="1.0" weight="3">\n'
            op += '\t\t<parameter idref="exponential.growthRate"/>\n'
            op += '\t</randomWalkOperator>\n'                    
        op += '\t<upDownOperator scaleFactor="0.75" weight="5.0">\n'
        op += '\t\t<up>'
        op += '<parameter idref="clock.rate"/>'
        op += '</up>\n'
        op += '\t\t<down>'
        op += '<parameter idref="treeModel.allInternalNodeHeights"/>'
        op += '</down>\n'
        op += '\t</upDownOperator>\n'        
        if datatype == "biallelicBinary":
            op += '\t<scaleOperator scaleFactor="0.25" weight="0.25">\n'
            op += '\t\t<parameter idref="biallelicBinary.demethylation"/>\n'
            op += '\t</scaleOperator>\n'
            op += '\t<scaleOperator scaleFactor="0.25" weight="0.25">\n'
            op += '\t\t<parameter idref="biallelicBinary.homozygousMethylation"/>\n'
            op += '\t</scaleOperator>\n'
            op += '\t<scaleOperator scaleFactor="0.25" weight="0.25">\n'
            op += '\t\t<parameter idref="biallelicBinary.homozygousDemethylation"/>\n'
            op += '\t</scaleOperator>\n'
        op += '</operators>\n'                                
        return op
    