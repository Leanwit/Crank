from pony.orm import *


db = Database()


class Documento(db.Entity):
    id = Required(int)
    url = Required(str)
    archivo = Required(str)
    Target = Set('Documento', reverse='Target')
    PrimaryKey(id, url)


import settings_db

db.generate_mapping(create_tables=True)
