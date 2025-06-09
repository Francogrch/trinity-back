from src.models import database, seed, seed_ciudades
import resetImagenes

def resetdb():
    database.reset_db()
    resetImagenes.run()
    seed_ciudades.run()
    seed.run()
