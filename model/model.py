from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self._best_sol = []
        self._best_cost = float('inf')
        self._umidita_citta = {}  # Sarà il dizionario dal DAO
        self._citta = ["Genova", "Milano", "Torino"]

    def get_umidita_media_mese(self, mese):
        return MeteoDao.get_umidita_media_mese(mese)

    def calcola_sequenza(self,mese):
        self._umidita_citta = MeteoDao.get_dati_ricorsione(mese)
        for citta in self._citta:
            if len(self._umidita_citta.get(citta, [])) < 15:
                # Se mancano dati, stampiamo un errore e usciamo senza far partire la ricorsione
                print(f"Errore: Dati mancanti per la città di {citta} nel mese {mese}")
                return None, None  # O gestisci l'errore come preferisci

        self._best_sol = []
        self._best_cost = float('inf')
        self._ricorsione([])
        return self._best_sol, self._best_cost

    def _ricorsione(self, parziale: []):
        livello = len(parziale)
        if livello == 15:
            if self._vincolo_3_giorni_valido(parziale):
                costo = self._calcola_costo(parziale)
                if costo < self._best_cost:
                    self._best_cost = costo
                    self._best_sol = list(parziale)
            return
        else:
            citta_possibili = self._get_citta_lecite(parziale)
            for c in citta_possibili:
                parziale.append(c)
                self._ricorsione(parziale)  # Ricorsione al livello successivo
                parziale.pop()

    def _get_citta_lecite(self, parziale):
        res = []
        livello = len(parziale)

        for c in self._citta:
            # VINCOLO 1: Massimo 6 giorni totali per città
            if parziale.count(c) >= 6:
                continue

            # VINCOLO 2: Permanenza minima 3 giorni consecutivi
            if livello > 0 and livello < 3:
                # Se siamo all'inizio (giorno 2 o 3), dobbiamo restare nella stessa città
                if c != parziale[0]:
                    continue

            if livello >= 3:
                # Se il tecnico è in una città da meno di 3 giorni, deve restare
                # Controlliamo se gli ultimi due giorni sono uguali all'ultimo inserito
                ultima_citta = parziale[-1]
                if parziale[-1] != parziale[-2] or parziale[-2] != parziale[-3]:
                    # Se non sono tutti e tre uguali, il tecnico è "bloccato"
                    if c != ultima_citta:
                        continue

            res.append(c)
        return res

    def _vincolo_3_giorni_valido(self, parziale):
        # Controlla che l'ultima città nella sequenza sia lì da almeno 3 giorni
        # (altrimenti la sequenza non è tecnicamente conclusa correttamente)
        if parziale[-1] == parziale[-2] and parziale[-2] == parziale[-3]:
            return True
        return False

    def _calcola_costo(self, parziale):
        costo = 0
        for i in range(len(parziale)):
            citta_attuale = parziale[i]
            # 1. Costo variabile: umidità del giorno i (indice i della lista)
            costo += self._umidita_citta[citta_attuale][i]

            # 2. Costo fisso: spostamento (100)
            if i > 0 and parziale[i] != parziale[i - 1]:
                costo += 100
        return costo