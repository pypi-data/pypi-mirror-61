import pandas as pd
from ..navegacion.conexiones import Impala
from ..config import PasesConfig, NavegacionConfig


# Errores custom para gestionar el ingreso correcto de los datos
class PasesListException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


# Errores custom para gestionar el ingreso correcto de los datos
class DataException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)



class ColumnException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


# Clase correspondiente a la extracción de información de los pases
class PaseUsuarioBp(object):
    def __init__(self):
        self._data_frame_list = []
        self._config = PasesConfig()

    # Para la lista de pases recibidas creamos batch de a 10000 y generamos el dataframe.
    def get_data(self, pases_id_list=None):
        if pases_id_list is not None:
            batch_pases_id = self.chunks(pases_id_list, self._config.CHUNK_SIZE)
            for batch in batch_pases_id:
                result = Impala().execute(self._config.PASES_QUERY.format(tuple(batch)))
                self._data_frame_list.append(result)
            return pd.concat(self._data_frame_list)
        else:
            raise PasesListException('La lista de pases enviada se encuentra vacía.')

    @staticmethod
    # Create a function called "chunks" with two arguments, l and n:
    def chunks(l, n):
        # For item i in a range that is a length of l,
        for i in range(0, len(l), n):
            # Create an index range for l of n items:
            yield l[i:i+n]

# Clase correspondiente a la extracción de información de los pases
class PaseSuscriptores(object):
    def __init__(self):
        self._config = NavegacionConfig()

    # Para la lista de pases recibidas creamos batch de a 10000 y generamos el dataframe.
    def get_data(self, fecha=None):
        if fecha is not None:
            print(fecha)
            return Impala().execute(self._config.SUSCRIPTORES_QUERY.format(fecha))
        else:
            raise PasesListException('Falta definir la fecha de la query.')


class NavegacionPases(object):
    def __init__(self):
        self._config = NavegacionConfig()

    # Para la lista de pases recibidas creamos batch de a 10000 y generamos el dataframe.
    def get_data(self, fecha=None):
        if fecha is not None:
            print(fecha)
            return Impala().execute(self._config.NAVEGACION_QUERY.format(fecha))
        else:
            raise PasesListException('Falta definir la fecha de la query.')