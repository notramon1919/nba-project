import os
import shutil
import subprocess
from pathlib import Path

import pandas as pd

from create_gifs.classes.Game import Game


def extract_7zip(file_path: Path, target_path: Path, password=None, remove_original=False):
    if isinstance(password, str):
        password = [password]
    for pwd in password:
        cmd = [shutil.which('7z'), 'x',
               f'-p{pwd}', f'-o{target_path}', file_path]
        process = subprocess.run(cmd, capture_output=True)
        if process.returncode == 0:
            if remove_original:
                file_path.unlink()
            break


def create_folders(game_name, to_create):
    for folder in to_create:
        if os.path.exists(f"./{game_name}_{folder}"):
            shutil.rmtree(f"./{game_name}_{folder}")
            os.makedirs(f"./{game_name}_{folder}")
        else:
            os.makedirs(f"./{game_name}_{folder}")
    pass


def event_save_gif(path_json, event_index, gif_folder):
    try:
        game = Game(path_json, event_index, gif_folder)
        game.read_json()
        game.save()
    except IndexError:
        print("Error. Posible evento vacío")

GAME_NAME = input("Código del partido: ")
OPTION = input("GIFS(0) o CSVS(1) ")

GIFS_FOLDER = f"./{GAME_NAME}_gifs"
CSVS_FOLDER = f"./{GAME_NAME}_csvs"
JSONS_FOLDER = f"./jsons"
JSON_GAME_FOLDER = f"./jsons/{GAME_NAME}"

if int(OPTION) == 0:
    create_folders(GAME_NAME, ["gifs"])
elif int(OPTION) == 1:
    create_folders(GAME_NAME, ["csvs"])
print("Carpetas creadas.")

if not os.path.exists(f"{JSON_GAME_FOLDER}"):
    extract_7zip(Path(f"data/2016.NBA.Raw.SportVU.Game.Logs/{GAME_NAME}.7z"), Path(f"{JSON_GAME_FOLDER}"),
                 password="")
    print("JSON Extraído")

JSON_PATH = JSON_GAME_FOLDER + "/" + os.listdir(f"{JSONS_FOLDER}/{GAME_NAME}")[0]
AMOUNT_EVENTS = len(pd.read_json(JSON_PATH))
print(f"Cantidad eventos: {AMOUNT_EVENTS}")

if int(OPTION) == 0:

    if input("Uno en concreto? (y/n): ").lower() == "y":
        evento_index = input("Número de evento: ")
        event_save_gif(path_json=JSON_PATH, event_index=int(evento_index), gif_folder=GIFS_FOLDER)
        print("Terminado")
    else:
        for EVENT in range(0, AMOUNT_EVENTS):
            print(f"Comenzando evento {EVENT + 1}...")
            event_save_gif(path_json=JSON_PATH, event_index=EVENT, gif_folder=GIFS_FOLDER)
            print(f"Evento {EVENT + 1} terminado.")

elif int(OPTION) == 1:

    game = Game(path_to_json=JSON_PATH)
    df_events = game.get_events().to_frame()
    df_events = pd.json_normalize(df_events['events'])
    df_events = df_events.reset_index()

    rows = []
    for idx, event in df_events.iterrows():
        moments = event['moments']
        if len(moments) > 10:
            for moment in moments:

                try:
                    rows.append({

                        "posession_clock": moment[3],

                        "ball_x": moment[5][0][2],
                        "ball_y": moment[5][0][3],
                        "ball_radius": moment[5][0][4],

                        "player_1_x": moment[5][1][2],
                        "player_1_y": moment[5][1][3],

                        "player_2_x": moment[5][2][2],
                        "player_2_y": moment[5][2][3],

                        "player_3_x": moment[5][3][2],
                        "player_3_y": moment[5][3][3],

                        "player_4_x": moment[5][4][2],
                        "player_4_y": moment[5][4][3],

                        "player_5_x": moment[5][5][2],
                        "player_5_y": moment[5][5][3],

                        "player_6_x": moment[5][6][2],
                        "player_6_y": moment[5][6][3],

                        "player_7_x": moment[5][7][2],
                        "player_7_y": moment[5][7][3],

                        "player_8_x": moment[5][8][2],
                        "player_8_y": moment[5][8][3],

                        "player_9_x": moment[5][9][2],
                        "player_9_y": moment[5][9][3],

                        "player_10_x": moment[5][10][2],
                        "player_10_y": moment[5][10][3],

                    })
                except IndexError:
                    continue

            df_event = pd.DataFrame(rows)
            file_count = len(os.listdir(CSVS_FOLDER))
            df_event.to_csv(f"{CSVS_FOLDER}/event_{file_count}.csv", index=False, float_format='%.4f')

            rows = []
            print(f"Evento {idx} terminado")
        else:
            print(f"Evento {idx} estaba vacío")
