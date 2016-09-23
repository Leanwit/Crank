from pony.orm import *

def obtenerCredenciales(db):
    db.bind("mysql", host="", user="", passwd="", db="")
    db.generate_mapping(create_tables=True)
