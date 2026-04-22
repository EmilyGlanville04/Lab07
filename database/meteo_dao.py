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
                result[row["Localita"]] = row["Media"]
            cursor.close()
            cnx.close()
        return result
