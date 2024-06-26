import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_grafo(self, e):
        anno=self._view.dd_anno.value
        if anno is None:
            self._view.create_alert("Selezionare un anno")
            return
        grafo = self._model.creaGrafo( int(anno))
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumNodes()} nodi."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumEdges()} archi."))
        for nodo in grafo.nodes:
            self._view.dd_direttore.options.append(ft.dropdown.Option(
                text=nodo))
        self._view.update_page()


    def handle_adiacenti(self, e):
        direttore = self._view.dd_direttore.value
        if direttore is None:
            self._view.create_alert("Selezionare un direttore")
            return
        lista=self._model.getadiacenti(direttore)
        for (regista,peso) in lista:
            self._view.txt_result.controls.append(ft.Text(f"{regista} - #attori condivisi: {peso}"))
        self._view.update_page()
    def filldd(self):
            ann = "200"
            for i in range(4, 7):
                anno = ann + str(i)
                self._view.dd_anno.options.append(ft.dropdown.Option(
                    text=anno))