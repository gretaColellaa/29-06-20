import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._attori = []
        self._idMapDirectors = {}
        self._nodes = []
        self._edges = []
        self._grafo = nx.DiGraph()
        self._mapPeso = {}

        self._mapAttori = {}

    def crea_grafo(self, anno):

        directors = DAO.getNodes(anno)
        for d in directors:
            self._idMapDirectors[d.id] = d
            self._nodes.append(d.id)
            self._mapAttori[d.id] = []

        lista = DAO.getAttoriDirectors(anno)
        for attore, regista in lista:
            if regista in self._mapAttori.keys():
                self._mapAttori[regista].append(attore)
            else:
                self._mapAttori[regista] = [attore]

            if attore not in self._attori :
                self._attori.append(attore)

        for a in self._attori:
            for n1 in self._nodes:
                for n2 in self._nodes:
                        if n1!=n2 and a in self._mapAttori[n1] and a in self._mapAttori[n2]:
                            if (n1,n2) in self._mapPeso.keys():
                                self._mapPeso[(n1,n2)]+=1
                            elif  (n2,n1) in self._mapPeso.keys():
                                self._mapPeso[(n2,n1)] += 1

                            else:
                                self._mapPeso[(n1, n2)] = 1

        for u,v in self._mapPeso.keys():
            self._edges.append((u,v,{'weight': self._mapPeso[(u,v)]}))


        self._grafo.add_nodes_from(self._nodes)
        self._grafo.add_edges_from(self._edges)


    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)

