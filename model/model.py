from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        pass

    def get_umidita_media_mese(self, mese):
        return MeteoDao.get_umidita_media_mese(mese)