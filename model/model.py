import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self._idMap = {}

    def creaGrafo(self, anno):
        self.nodi = DAO.getNodi(anno)
        self.grafo.add_nodes_from(self.nodi)
        for v in self.nodi:
            self._idMap[v.id] = v
        self.addEdges(anno)
        return self.grafo

    def getNumNodes(self):
        return len(self.grafo.nodes)

    def getNumEdges(self):
        return len(self.grafo.edges)

    def addEdges(self, anno):
        self.grafo.clear_edges()
        allEdges = DAO.getConnessioni(anno)
        for connessione in allEdges:
            nodo1 = self._idMap[connessione.v1]
            nodo2 = self._idMap[connessione.v2]
            if nodo1 in self.grafo.nodes and nodo2 in self.grafo.nodes:
                if self.grafo.has_edge(nodo1, nodo2) == False:
                    self.grafo.add_edge(nodo1, nodo2, weight=connessione.peso)

    def getadiacenti(self, direttoreStringa):
        lista=[]
        direttoreid=direttoreStringa.split("-")[0]
        direttore=self._idMap[int(direttoreid)]
        for nodo in self.grafo.neighbors(direttore):
            lista.append((nodo,self.grafo[nodo][direttore]["weight"]))
        return sorted(lista,key=lambda x:x[1], reverse=True)
