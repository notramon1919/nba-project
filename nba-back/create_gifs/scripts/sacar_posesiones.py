import os
import shutil

import pandas as pd
import py7zr
from pandas import DataFrame


def dividir_en_posesiones(df_event) -> list[DataFrame]:
    posesiones = []
    posesion_actual = []
    reloj_anterior = 0

    if not df_event["possession_clock"].isnull().any():
        for _, fila in df_event.iterrows():
            reloj_actual = fila["possession_clock"]

            if reloj_actual is None:
                reloj_actual = reloj_anterior - 0.0400

            elif reloj_actual > reloj_anterior:
                if posesion_actual:
                    posesiones.append(pd.DataFrame(posesion_actual))
                    posesion_actual = []

            posesion_actual.append(fila)
            reloj_anterior = reloj_actual

        if posesion_actual:
            posesiones.append(pd.DataFrame(posesion_actual))
    else:
        print("Nulos en possession clock")

    return posesiones


def unir_posesiones(posesiones_folder):
    csvs_solapados = 0
    archivos = sorted(os.listdir(posesiones_folder))
    i = 0

    print()
    print("Posesiones antes:", len(archivos))
    print("Uniendo Duplicados o Separados")

    while i < len(archivos) - 1:
        actual_path = os.path.join(posesiones_folder, archivos[i])
        siguiente_path = os.path.join(posesiones_folder, archivos[i + 1])

        df_actual = pd.read_csv(actual_path)
        df_siguiente = pd.read_csv(siguiente_path)

        primera_fila_siguiente = df_siguiente.iloc[0]

        match_idx = df_actual[df_actual.eq(primera_fila_siguiente).all(axis=1)].index

        if not match_idx.empty:
            idx = match_idx[0]

            df_merged = pd.concat([df_actual.iloc[:idx], df_siguiente], ignore_index=True)

            merged_filename = os.path.join(posesiones_folder,
                                           f"{GAME_NAME.split(".")[3]}-{GAME_NAME.split(".")[5]}_{posesion_counter:04d}.csv")
            df_merged.to_csv(merged_filename, index=False, float_format="%.4f")

            os.remove(actual_path)
            os.remove(siguiente_path)

            archivos = sorted(os.listdir(posesiones_folder))
            i = 0
            csvs_solapados += 1
        else:
            i += 1

    print("Posesiones después:", len(archivos))
    print("CSVs solapados:", csvs_solapados)


GAME_NAME = input("Código de partido: ")
POSESIONES_FOLDER = f"../data/csv_posesiones/{GAME_NAME}"
JSONS_FOLDER = f"../data/jsons/{GAME_NAME}"

if os.path.exists(POSESIONES_FOLDER):
    shutil.rmtree(POSESIONES_FOLDER)
os.makedirs(POSESIONES_FOLDER)

if os.path.exists(JSONS_FOLDER):
    shutil.rmtree(JSONS_FOLDER)
os.makedirs(JSONS_FOLDER)

if len(os.listdir(JSONS_FOLDER)) != 0:
    JSON_PATH = f"{JSONS_FOLDER}/{os.listdir(f'{JSONS_FOLDER}')[0]}"
else:
    archive = py7zr.SevenZipFile(f"../data/2016.NBA.Raw.SportVU.Game.Logs/{GAME_NAME}.7z", mode='r')
    archive.extractall(path=f"{JSONS_FOLDER}")

    JSON_PATH = f"{JSONS_FOLDER}/{os.listdir(f'{JSONS_FOLDER}')[0]}"

df = pd.read_json(JSON_PATH)
events = df["events"]
df_events = events.to_frame()
df_events = pd.json_normalize(df_events['events'])
df_events = df_events.reset_index()

posesion_counter = len(os.listdir(POSESIONES_FOLDER))
game_timers = []

for idx, event in df_events.iterrows():
    moments = event['moments']

    if len(moments) > 10:
        rows = []
        for moment in moments:
            try:
                rows.append({

                    "game_timer": moment[2],
                    "possession_clock": moment[3],
                    "ball_x": moment[5][0][2], "ball_y": moment[5][0][3], "ball_radius": moment[5][0][4],

                    "player_1_x": moment[5][1][2], "player_1_y": moment[5][1][3],

                    "player_2_x": moment[5][2][2], "player_2_y": moment[5][2][3],

                    "player_3_x": moment[5][3][2], "player_3_y": moment[5][3][3],

                    "player_4_x": moment[5][4][2], "player_4_y": moment[5][4][3],

                    "player_5_x": moment[5][5][2], "player_5_y": moment[5][5][3],

                    "player_6_x": moment[5][6][2], "player_6_y": moment[5][6][3],

                    "player_7_x": moment[5][7][2], "player_7_y": moment[5][7][3],

                    "player_8_x": moment[5][8][2], "player_8_y": moment[5][8][3],

                    "player_9_x": moment[5][9][2], "player_9_y": moment[5][9][3],

                    "player_10_x": moment[5][10][2], "player_10_y": moment[5][10][3],

                })
            except IndexError:
                continue

        df_event = pd.DataFrame(rows)
        posesiones = dividir_en_posesiones(df_event)

        for posesion in posesiones:
            if len(posesion) > 0:
                inicio = posesion["game_timer"].iloc[0]
                fin = posesion["game_timer"].iloc[-1]
                key = (inicio, fin)

                if key not in game_timers:
                    game_timers.append(key)

                    if len(posesion) > 60:
                        filename = f"{POSESIONES_FOLDER}/{GAME_NAME.split(".")[3]}-{GAME_NAME.split(".")[5]}_{posesion_counter:04d}.csv"
                        posesion.to_csv(filename, index=False, float_format="%.4f")
                        posesion_counter += 1
                    else:
                        print("La posesión no es lo suficientemente extensa")
                else:
                    print(f"Posesión duplicada: inicio {inicio}, fin {fin}")
        print(f"Evento {idx} terminado ({len(posesiones)} posesiones)")
    else:
        print(f"Evento {idx} estaba vacío")

unir_posesiones(POSESIONES_FOLDER)
