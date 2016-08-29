from pony.orm import *

def obtenerCredenciales(db):
    db.bind("mysql", host="localhost", user="root", passwd="motocross1", db="Crank")
    db.generate_mapping(create_tables=True)
