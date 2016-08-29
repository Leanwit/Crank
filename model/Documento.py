from pony.orm import *
from settings_db import *

db = Database()


class Documento(db.Entity):
    id = Required(int)
    url = Required(str)
    archivo = Required(str)
    Target = Set('Documento', reverse='Target')
    PrimaryKey(id, url)

obtenerCredenciales(db)
