import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._attori = []
        self._idMapDirectors = {}
        self._nodes = []
        self._edges = []
        self._grafo = nx.Graph()
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
                print(n1)
                for n2 in self._nodes:
                        if n1!=n2 and a in self._mapAttori[n1] and a in self._mapAttori[n2]:
                            if (n1,n2) in self._mapPeso.keys():
                                self._mapPeso[(n1,n2)]+=1
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

    def getAdiacenti(self, nodo):
        nodo = int(nodo)
        ad_ordinati = []

        for a in self._grafo.neighbors(nodo):
            edge_data = self._grafo.get_edge_data(nodo, a)
            if edge_data is None:
                edge_data = self._grafo.get_edge_data(a, nodo)
            if edge_data is not None and 'weight' in edge_data:
                peso = int(edge_data['weight'])
                ad_ordinati.append((a, peso))
            else:
                print(f"Attenzione: arco mancante o senza peso tra {nodo} e {a}")

        return sorted(ad_ordinati, key=lambda x: x[1], reverse=True)

    def cerca_cammino(self, partenza, c):
        self._best_cammino = []
        self._best_peso = 0
        self._ricorsione([partenza], 0, {partenza}, c)
        return self._best_cammino, self._best_peso

    def _ricorsione(self, cammino_parziale, peso_parziale, visited, c):
        ultimo = cammino_parziale[-1]

        # Caso finale: aggiorna se questo cammino è migliore
        if peso_parziale <= c:
            self._best_peso = peso_parziale
            self._best_cammino = list(cammino_parziale)

        for vicino in self._grafo.neighbors(ultimo):
            if vicino not in visited:
                peso = self._grafo[ultimo][vicino]['weight']

                visited.add(vicino)
                cammino_parziale.append(vicino)

                self._ricorsione(cammino_parziale, peso_parziale + peso, visited,c)

                # Backtrack
                visited.remove(vicino)
                cammino_parziale.pop()


