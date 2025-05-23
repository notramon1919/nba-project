import csv
import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'clave_secreta'

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


# === User Class ===
class User(UserMixin):
    def __init__(self, username):
        self.id = username


# === Cargar usuario desde CSV ===
def load_users():
    users = {}
    with open('usuarios.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            users[row['username']] = {
                'password': row['password'],
                'etiquetado_completado': row.get('etiquetado_completado', 'false') == 'true'
            }
    return users


USERS = load_users()


@login_manager.user_loader
def load_user(user_id):
    if user_id in USERS:
        return User(user_id)
    return None


# === LOGIN ===
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username in USERS and USERS[username]['password'] == password:
        user = User(username)
        login_user(user)
        completado = USERS[username].get('etiquetado_completado')
        if completado:
            return jsonify({'success': False, 'message': 'Este usuario ya ha etiquetado todos los GIFs'}), 401
        return jsonify({'success': True, 'user': username, 'etiquetado_completado': completado})
    return jsonify({'success': False, 'message': 'Credenciales inválidas'}), 401


def set_completado(username):
    rows = []
    with open('usuarios.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['username'] == username:
                row['etiquetado_completado'] = 'true'
            rows.append(row)

    with open('usuarios.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = rows[0].keys() if rows else ['username', 'password', 'etiquetado_completado']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Recarga usuarios global
    global USERS
    USERS = load_users()

# === EXPERIENCIA ===
@app.route('/form', methods=['POST'])
@login_required
def form():
    data = request.json
    expe1 = data.get('expe1')
    nivel1 = data.get('nivel1')
    expe2 = data.get('expe2')
    nivel2 = data.get('nivel2')

    file_path = 'experiencia.csv'
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists or os.path.getsize(file_path) == 0:
            writer.writerow(["experiencia-jugador", "nivel-jugador", "experiencia-entrenador", "nivel-entrenador"])
        writer.writerow([expe1, nivel1, expe2, nivel2])

    return {'status': 'ok'}

# === LOGOUT ===
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'success': True})


# === Ruta protegida de gifs ===
@app.route('/gifs', methods=['GET'])
@login_required
def get_gif_list():
    gif_folder = 'static/gifs_posesiones'
    gif_files = []

    registered_gifs = set()
    if os.path.isfile('data.csv'):
        with open('data.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                registered_gifs.add(row['nombre'])

    for root, dirs, files in os.walk(gif_folder):
        for file in files:
            if file.endswith('.gif'):
                if file not in registered_gifs:
                    relative_path = os.path.relpath(os.path.join(root, file), 'static')
                    gif_files.append(relative_path.replace("\\", "/"))

    gif_files.sort()
    return jsonify({'gifs': gif_files})


# === Ruta protegida para submit ===
@app.route('/submit', methods=['POST'])
@login_required
def submit():
    data = request.json
    gif = data.get('gif').split("/")[2]
    valido = data.get('valido')
    descripcion = data.get('descripcion')
    equipo = data.get('equipo')
    etiquetado_por = current_user.id

    file_path = 'data.csv'
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists or os.path.getsize(file_path) == 0:
            writer.writerow(["nombre", "es_valido", "descripcion", "equipo", "etiquetado_por"])
        writer.writerow([gif, valido, descripcion, equipo, etiquetado_por])

    # Contar cuantos gifs ha etiquetado
    count = 0
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['etiquetado_por'] == etiquetado_por:
                count += 1

    if count >= 30:
        set_completado(etiquetado_por)

    return {'status': 'ok'}


if __name__ == '__main__':
    app.run(debug=True)
