#https://biopython.org/wiki/Phylo
#https://biopython.org/wiki/PhyloXML
#https://www.youtube.com/watch?v=wBdz3vFQ4Ks
#https://biopython.org/wiki/Phylo_cookbook
#https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-13-209/tables/1




class PhyloTree(object):
    def __init__(self,nexus_string):
        self.nexus = nexus_string
        self.xmltree = None
        
    def get_tree(self):
        """_summary_
        Converts nexus string to xml string
        But is currently hardcoded
        """        
        #Phylo.draw_ascii(tree)                    
        #netx = Phylo.to_networkx(tree)
        #print(netx)
        #import networkx as nx
        #from networkx.drawing.nx_pydot import graphviz_layout            
        #pos = graphviz_layout(netx, prog="dot")
        #st.pyplot(nx.draw(netx, pos))
            
        
        