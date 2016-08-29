from pony.orm import *
from settings_db import *

db = Database()


class Documento(db.Entity):
    id = PrimaryKey(int,auto=True)
    url = Required(str)
    archivo = Optional(str)
    Target = Set('Documento', reverse='Target')

    #atributos no persistidos
    scoreRelevance = 0
    scoreContribution = 0
    scoreFinal = 0

obtenerCredenciales(db)
