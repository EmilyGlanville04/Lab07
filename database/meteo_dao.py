from database.DB_connect import DBConnect
from model.situazione import Situazione


class MeteoDao():

    @staticmethod
    def get_all_situazioni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s 
                        ORDER BY s.Data ASC"""
            cursor.execute(query)
            for row in cursor:
                #CREARE UNA LISTA DI OGGETTI
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_umidita_media_mese(mese):
        cnx = DBConnect.get_connection()
        result = {}
        if cnx is not None:
            cursor = cnx.cursor(dictionary=True)
            # Query che raggruppa per città e calcola la media nel mese scelto
            query = """SELECT Localita, AVG(Umidita) as Media
                           FROM situazione 
                           WHERE MONTH(Data) = %s
                           GROUP BY Localita"""
            cursor.execute(query, (mese,))
            for row in cursor:
                #CREARE UN DIZIONARIO
                result[row["Localita"]] = row["Media"]
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_dati_ricorsione(mese):
        cnx = DBConnect.get_connection()
        result = {
            "Genova":[],
            "Milano":[],
            "Torino":[]
        }
        if cnx is not None:
            cursor = cnx.cursor(dictionary=True)
            # Query che raggruppa per città e calcola la media nel mese scelto
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s 
                        WHERE MONTH(s.Data) = %s AND DAY(s.Data) <= 15
                        ORDER BY s.Localita , s.Data asc"""
            cursor.execute(query, (mese,))
            for row in cursor:
                localita= row["Localita"]
                umidita=row["Umidita"]
                result[localita].append(umidita)
            cursor.close()
            cnx.close()
        return result
