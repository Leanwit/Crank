from pony.orm import *
from settings_db import *

db = Database()


class Documento(db.Entity):
    id = PrimaryKey(int,auto=True)
    url = Required(str)
    archivo = Optional(str)
    Target = Set('Documento', reverse='Target')

obtenerCredenciales(db)
