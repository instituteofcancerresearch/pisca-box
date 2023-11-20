
import datetime
import random
import streamlit as st


class Session():
    """All the files this session will use
    
    NOT CURRENTLY USED

    """    
    def __init__(self):
        if "session" not in st.session_state:
            self.then = str(datetime.datetime.now())
            self.rand = random.randint(0,1000000000000)
            self.session = f"{self.then}-{self.rand}-"  
        else:
            self.session = st.session_state["session"]
        
    def getBeautiFile(self):
        return f"{self.session}-out.out"
    
    def getOutFile(self):
        return f"{self.session}-out.out"
    
    def getLogFile(self):
        return f"{self.session}-log.log"
    
    def getTreeFile(self):
        return f"{self.session}-tree.tree"
    
    def getConsensusFile(self):
        return f"{self.session}-mcc.mcc"
    
    def getSVGFile(self):
        return f"{self.session}-svg.svg"

    
    

        