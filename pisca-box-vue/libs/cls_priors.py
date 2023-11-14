# ruff: noqa: E501
# ruff: noqa: F841
import pandas as pd

tab1 = ""
tab2 = "\t"
tab3 = "\t\t"
tab4 = "\t\t\t"
tab5 = "\t\t\t\t"

class Priors(object):
    def __init__(self,demographic,default_prs):
        self.demographic = demographic        
        self.priors = []
        ## default from the datatype
        self.priors.append(["coalescentLikelihood","coalescent","","","","","","","","",""])                        
        # from the demongraphic
        if self.demographic == "constant size":
            self.priors.append(["oneOnXPrior","constant.popSize","","","","","","","","",""])
        elif self.demographic == "exponential growth":        
            self.priors.append(["oneOnXPrior","exponential.popSize","","","","","","","","",""])
            self.priors.append(["laplacePrior","exponential.growthRate","","","0.0","","","","","1.0",""])
            
        for pr in default_prs:
            self.priors.append(pr)
        # from the clock
        #self.priors.append(clock_prior)
        #self.priors.append(luca_prior)                                
        """
        ------------------------------------------------------------------------------------------------------------------------------
        operator            parameter   lower   upper   mean    stddev  offset      meanInRealSpace     shape   scale   treeModel
        ------------------------------------------------------------------------------------------------------------------------------
        coalescentLikelihood param
        oneOnXPrior         param
        uniformPrior        param       lower   upper
        exponentialPrior    param                       mean            offset
        logNormalPrior      param                       mean    sd      offset      mirs
        normalPrior         param                       mean    sd      offset      mirs
        ctmcScalePrior      param                                                                                       treemod
        gammaPrior          param                                       offset                          shape   scale
        laplacePrior        param                       mean                                                    scale                        
        ------------------------------------------------------------------------------------------------------------------------------                
        # All the priors I know about
        ["coalescentLikelihood","coalescent","","","","","","","","",""]
        ## From biallelic binary
        ["oneOnXPrior","constant.popSize","","","","","","","","",""]
        ["uniformPrior","luca_branch","1.0","73.91491902959673","","","","","","",""]
        ["normalPrior","clock.rate","","","0.0","0.13","0.0","true","","",""]
        ["logNormalPrior","biallelicBinary.demethylation","","","1.0","0.6","0.0","true","","",""]
        ["logNormalPrior","biallelicBinary.homozygousMethylation","","","1.0","0.6","0.0","true","","",""]
        ["logNormalPrior","biallelicBinary.homozygousDemethylation","","","1.0","0.6","0.0","true","","",""]
        ## From acna examples
        ["oneOnXPrior","exponential.popSize","","","","","","","","",""]
        ["laplacePrior","exponential.growthRate","","","0.0","","","","","1.0",""]
        ["logNormalPrior","clock.rate","","","0.1","0.3","0.0","true","","",""]
        ["exponentialPrior","acna.loss","","","1.0","","0.0","","","",""]
        ["uniformPrior","luca_height","1.0","50","","","","","","",""]
        ["oneOnXPrior","constant.popSize","","","","","","","","",""]
        ["uniformPrior","luca_height","2.73999961035501","76.3799893509288","","","","","","",""]
        ## strict clock
        ["ctmcScalePrior","clock.rate","","","","","","","","","treeModel"]
        """
    def get_priors_xml(self):
        prs = f'{tab3}<prior id="prior">\n'
        for pr in self.priors:
            if pr[0] == "coalescentLikelihood":
                prs += self._coalescentLikelihood(pr)
            elif pr[0] == "oneOnXPrior":
                prs += self._oneOnXPrior(pr)
            elif pr[0] == "uniformPrior":
                prs += self._uniformPrior(pr)
            elif pr[0] == "exponentialPrior":
                prs += self._exponentialPrior(pr)
            elif pr[0] == "logNormalPrior":
                prs += self._logNormalPrior(pr)
            elif pr[0] == "normalPrior":
                prs += self._normalPrior(pr)
            elif pr[0] == "ctmcScalePrior":
                prs += self._ctmcScalePrior(pr)
            elif pr[0] == "gammaPrior":
                prs += self._gammaPrior(pr)
            elif pr[0] == "laplacePrior":
                prs += self._laplacePrior(pr)            
        prs += f'{tab3}</prior>\n'
        return prs            
    #########################################################################################
    def getPriorsList(self):
        #create list from priors and operators
        prs = []
        for pr in self.priors:
            if pr[1] not in prs:
                prs.append(pr[1])
        return prs    
    #########################################################################################def _coalescentLikelihood(self,pr):
        op,prm,lwr,upr,men,std,off,mns,shp,scl,tree = pr[0],pr[1],pr[2],pr[3],pr[4],pr[5],pr[6],pr[7],pr[8],pr[9],pr[10]
        prx = ""
        prx += f'{tab4}<coalescentLikelihood idref="{prm}"/>\n'
        return prx
    #-------------------------------------------------------------------------------------------------------------------
    def _coalescentLikelihood(self,pr):
        op,prm,lwr,upr,men,std,off,mns,shp,scl,tree = pr[0],pr[1],pr[2],pr[3],pr[4],pr[5],pr[6],pr[7],pr[8],pr[9],pr[10]
        prx = ""
        prx += f'{tab4}<coalescentLikelihood idref="{prm}"/>\n'        
        return prx
    #-------------------------------------------------------------------------------------------------------------------
    def _oneOnXPrior(self,pr):
        op,prm,lwr,upr,men,std,off,mns,shp,scl,tree = pr[0],pr[1],pr[2],pr[3],pr[4],pr[5],pr[6],pr[7],pr[8],pr[9],pr[10]
        prx = ""
        prx += f'{tab4}<oneOnXPrior>\n'
        prx += f'{tab5}<parameter idref="{prm}"/>\n'
        prx += f'{tab4}</oneOnXPrior>\n'                    
        return prx
    #-------------------------------------------------------------------------------------------------------------------
    def _uniformPrior(self,pr):
        op,prm,lwr,upr,men,std,off,mns,shp,scl,tree = pr[0],pr[1],pr[2],pr[3],pr[4],pr[5],pr[6],pr[7],pr[8],pr[9],pr[10]
        prx = ""                
        prx += f'{tab4}<uniformPrior lower="{lwr}" upper="{upr}">\n'
        prx += f'{tab5}<parameter idref="{prm}"/>\n'
        prx += f'{tab4}</uniformPrior>\n'        
        return prx
    #-------------------------------------------------------------------------------------------------------------------
    def _exponentialPrior(self,pr):
        op,prm,lwr,upr,men,std,off,mns,shp,scl,tree = pr[0],pr[1],pr[2],pr[3],pr[4],pr[5],pr[6],pr[7],pr[8],pr[9],pr[10]
        prx = ""
        prx += f'{tab4}<exponentialPrior mean="{men}" offset="{off}">\n'
        prx += f'{tab5}<parameter idref="{prm}"/>\n'
        prx += f'{tab4}</exponentialPrior>\n'
        return prx
    #-------------------------------------------------------------------------------------------------------------------
    def _logNormalPrior(self,pr):
        op,prm,lwr,upr,men,std,off,mns,shp,scl,tree = pr[0],pr[1],pr[2],pr[3],pr[4],pr[5],pr[6],pr[7],pr[8],pr[9],pr[10]
        prx = ""                          
        prx += f'{tab4}<logNormalPrior mean="{men}" stdev="{std}" offset="{off}" meanInRealSpace="{str(mns).lower()}">\n'
        prx += f'{tab5}<parameter idref="{prm}"/>\n'
        prx += f'{tab4}</logNormalPrior>\n'
        return prx            
    #-------------------------------------------------------------------------------------------------------------------
    def _normalPrior(self,pr):
        op,prm,lwr,upr,men,std,off,mns,shp,scl,tree = pr[0],pr[1],pr[2],pr[3],pr[4],pr[5],pr[6],pr[7],pr[8],pr[9],pr[10]
        prx = ""                          
        prx += f'{tab4}<normalPrior mean="{men}" stdev="{std}" offset="{off}" meanInRealSpace="{str(mns).lower()}">\n'
        prx += f'{tab5}<parameter idref="{prm}"/>\n'
        prx += f'{tab4}</normalPrior>\n'
        return prx            
    #-------------------------------------------------------------------------------------------------------------------
    def _ctmcScalePrior(self,pr):
        op,prm,lwr,upr,men,std,off,mns,shp,scl,tree = pr[0],pr[1],pr[2],pr[3],pr[4],pr[5],pr[6],pr[7],pr[8],pr[9],pr[10]
        prx = ""        
        prx += f'{tab4}<ctmcScalePrior>\n'
        prx += f'{tab5}<ctmcScale><parameter idref="{prm}"/></ctmcScale>\n'
        prx += f'{tab5}<treeModel idref="{tree}"/>\n'
        prx += f'{tab4}</ctmcScalePrior>\n'
        return prx
    #-------------------------------------------------------------------------------------------------------------------
    def _gammaPrior(self,pr):
        op,prm,lwr,upr,men,std,off,mns,shp,scl,tree = pr[0],pr[1],pr[2],pr[3],pr[4],pr[5],pr[6],pr[7],pr[8],pr[9],pr[10]
        prx = ""
        prx += f'{tab4}<gammaPrior shape="{shp}" scale="{scl}" offset="{off}">\n'
        prx += f'{tab5}<parameter idref="{prm}"/>\n'
        prx += f'{tab4}</gammaPrior>\n'
        return prx
    #-------------------------------------------------------------------------------------------------------------------
    def _laplacePrior(self,pr):
        op,prm,lwr,upr,men,std,off,mns,shp,scl,tree = pr[0],pr[1],pr[2],pr[3],pr[4],pr[5],pr[6],pr[7],pr[8],pr[9],pr[10]
        prx = ""
        prx += f'{tab4}<laplacePrior mean="{men}" scale="{scl}">\n'
        prx += f'{tab5}<parameter idref="{prm}"/>\n'
        prx += f'{tab4}</laplacePrior>\n'
        return prx
    #-------------------------------------------------------------------------------------------------------------------    
    def get_as_dataframe(self):                
        df = pd.DataFrame(self.priors,columns=['operator','parameter','lower','upper','mean','stddev','offset','meanInRealSpace','shape','scale','treeModel'])
        return df
    #---------------------------------------------------------------------------------
    def update_from_dataframe(self,df):
        self.priors = []
        for row in df.itertuples():        
            self.priors.append([row.operator,row.parameter,row.lower,row.upper,row.mean,row.stddev,row.offset,row.meanInRealSpace,row.shape,row.scale,row.treeModel])
    #-------------------------------------------------------------------------------------------------------------------
    def get_one_prior(self,prior_name):
        for pr in self.priors:
            if len(pr) > 0:
                if pr[1] == prior_name:
                    return pr
        return None
    #-------------------------------------------------------------------------------------------------------------------
    def update_one_prior(self,remove,prior_name,new_vals):
        updated = False
        prs = []
        for pr in self.priors:
            if len(pr) > 0:
                if pr[1] == prior_name and not remove:
                    updated = True
                    prs.append(new_vals)
                else:
                    prs.append(pr)
        if not updated and not remove:
            prs.append(new_vals)
        self.priors = prs
    #-------------------------------------------------------------------------------------------------------------------
        

    