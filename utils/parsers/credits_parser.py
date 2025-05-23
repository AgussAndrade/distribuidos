import ast
import csv

from model.actor import Actor


def convert_data(data):
    # data debe ser una lista de strings (líneas), no un string completo
    lines = data.get("cola", [])  # extrae lista de líneas desde el dict
    
    # Ignorar la primera línea que contiene los encabezados
    if lines and lines[0].startswith("cast,"):
        lines = lines[1:]

    reader = csv.DictReader(lines, fieldnames=["cast", "crew", "id"])

    # ir sumando los campos a medida que se usan
    result = []

    for row in reader:
        cast = row["cast"]
        cast_list = ast.literal_eval(cast)

        for actor in cast_list:
            result.append(Actor(
                id=actor["id"],
                name=actor["name"],
                movie_id=row["id"],
            ))
    return result






