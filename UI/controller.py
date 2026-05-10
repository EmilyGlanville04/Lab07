import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        self._view.lst_result.controls.clear()
        if self._mese == 0:
            self._view.create_alert("Selezionare un mese prima di procedere")
        risultati = self._model.get_umidita_media_mese(self._mese)
        self._view.lst_result.controls.append(ft.Text(f"L'umidità media nel mese selezionato è:"))
        for citta, media in risultati.items():
            self._view.lst_result.controls.append(ft.Text(f"{citta}: umidità media = {media}"))
        self._view.update_page()

    def handle_sequenza(self, e):
        if self._mese == 0:
            self._view.create_alert("Selezionare un mese")
            return
        sequenza_ottima, costo = self._model.calcola_sequenza(self._mese)
        if sequenza_ottima is None:
            self._view.lst_result.controls.append(
                ft.Text("Dati insufficienti nel database per completare l'analisi dei 15 giorni.", color="red")
            )
            self._view.update_page()
            return
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"La sequenza ottima ha costo {costo} ed è:"))
        for i, stop in enumerate(sequenza_ottima):
            self._view.lst_result.controls.append(ft.Text(f"Giorno {i + 1}: {stop}"))
        self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)

