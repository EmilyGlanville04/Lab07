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
        pass

    def read_mese(self, e):
        self._mese = int(e.control.value)

