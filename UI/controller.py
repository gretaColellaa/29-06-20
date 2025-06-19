import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAffini(self,e):
        try : int(self._view._txtCondivisi.value)
        except:  self._view.create_alert("inserire un numero intero")
        cammino, peso = self._model.cerca_cammino(int(self._view._ddDirector.value), int(self._view._txtCondivisi.value))
        self._view.txt_result.controls.append(ft.Text(f"Il gruppo più grande di {len(cammino)} registi a partire da"
                                                      f"{int(self._view._ddDirector.value)} con un totale di {peso} attori "
                                                      f"condivisi"))

        for r in cammino:
            self._view.txt_result.controls.append(ft.Text(f"{r}"))

        self._view.update_page()


    def handleAdiacenti(self,e):
        try: self._view._ddDirector.value
        except: self._view.create_alert("Selezionare un regista")

        ad = self._model.getAdiacenti(self._view._ddDirector.value)

        for a in ad:
            self._view.txt_result.controls.append(ft.Text(f"{a[0]} #attori condivisi: {a[1]}"))

        self._view.update_page()


    def handleCreaGrafo(self, e):
        if self._view._ddanno.value:
            self._model.crea_grafo(int(self._view._ddanno.value))

            self._view.txt_result.controls.append(ft.Text(f"il grafo ha {self._model.getNumNodes()} nodi"
                                                          f" e {self._model.getNumEdges()} archi"))

            nodi = self._model._nodes
            for n in sorted(nodi):
                # print(n)
                self._view._ddDirector.options.append(ft.dropdown.Option(n))

            self._view.update_page()

        else:
            self._view.create_alert("seleziona un anno")


    def fillDDanno(self):
        for i in range(2004,2007):
            self._view._ddanno.options.append(ft.dropdown.Option(str(i)))




