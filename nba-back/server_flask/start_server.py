import csv
import os

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/gifs', methods=['GET'])
def get_gif_list():
    gif_folder = 'static/gifs_posesiones'
    gif_files = []

    # Leer gifs ya registrados en data.csv
    registered_gifs = set()
    csv_path = 'data.csv'
    if os.path.isfile(csv_path):
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                registered_gifs.add(row['nombre'])

    # Recorrer gifs
    for root, dirs, files in os.walk(gif_folder):
        for file in files:
            if file.endswith('.gif'):
                gif_name = file
                if gif_name not in registered_gifs:
                    relative_path = os.path.relpath(os.path.join(root, file), 'static')
                    gif_files.append(relative_path.replace("\\", "/"))

    gif_files.sort()
    return jsonify({'gifs': gif_files})


@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    gif = data.get('gif').split("/")[2]  # NOMBRE_GIF: STRING
    valido = data.get('valido')  # VALIDO_O_NO: BOOLEAN
    descripcion = data.get('descripcion', '')  # DESCRIPCION: STRING
    etiquetado_por = data.get('etiquetado_por', '')  # ETIQUETADO_POR: STRING

    file_path = 'data.csv'
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Cabecera solo si el archivo no existe o está vacío
        if not file_exists or os.path.getsize(file_path) == 0:
            writer.writerow(["nombre", "es_valido", "descripcion", "etiquetado_por"])

        writer.writerow([gif, valido, descripcion, etiquetado_por])

    return {'status': 'ok'}


if __name__ == '__main__':
    app.run()
