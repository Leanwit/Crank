from pony.orm import *
from settings_db import *

db = Database()


class Documento(db.Entity):
    id = PrimaryKey(int,auto=True)
    url = Required(str)
    Target = Set('Documento', reverse='Target')
    # Atributos persistidos pero propios de cada corrida del algoritmo.
    scoreRelevance = Optional(float)
    scoreContribution = Optional(float)
    scoreFinal = Optional(float)


obtenerCredenciales(db)
