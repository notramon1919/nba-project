from flask import Flask, request, jsonify
import csv
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/gifs', methods=['GET'])
def get_gif_list():
    gif_folder = 'static/gifs'
    gif_files = sorted([f for f in os.listdir(gif_folder) if f.endswith('.gif')])
    return jsonify({'gifs': gif_files})


@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    gif = data.get('gif')  # NOMBRE_GIF: STRING
    valido = data.get('valido')  # VALIDO_O_NO: BOOLEAN
    descripcion = data.get('descripcion', '')  # DESCRIPCION: STRING

    file_path = 'data.csv'
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Cabecera solo si el archivo no existe o está vacío
        if not file_exists or os.path.getsize(file_path) == 0:
            writer.writerow(['nombre', 'es_valido', 'descripcion'])

        writer.writerow([gif, valido, descripcion])

    return {'status': 'ok'}


if __name__ == '__main__':
    app.run()
