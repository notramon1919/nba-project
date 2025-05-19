import matplotlib.animation as animation
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import PillowWriter
import os
import shutil


class Constant:
    PLAYER_CIRCLE_SIZE = 1.7
    INTERVAL = 40
    DIFF = 6
    X_MIN = 0
    X_MAX = 93.5
    Y_MIN = 0
    Y_MAX = 50
    X_CENTER = (X_MAX + X_MIN) / 2
    Y_CENTER = Y_MAX - DIFF / 1.5 - 0.35


def create_animation(df: pd.DataFrame, output_path: str):
    fig, ax = plt.subplots(figsize=(7.85, 4.2))

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_xlim(Constant.X_MIN, Constant.X_MAX)
    ax.set_ylim(Constant.Y_MIN, Constant.Y_MAX)
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')

    court = plt.imread('../assets/court.png')
    ax.imshow(
        court,
        zorder=0,
        extent=(Constant.X_MIN, Constant.X_MAX, Constant.Y_MIN, Constant.Y_MAX),
        origin='lower'
    )

    player_circles = [
                         plt.Circle((0, 0), Constant.PLAYER_CIRCLE_SIZE, color='red') for _ in range(5)
                     ] + [
                         plt.Circle((0, 0), Constant.PLAYER_CIRCLE_SIZE, color='blue') for _ in range(5)
                     ]
    ball_circle = plt.Circle((0, 0), Constant.PLAYER_CIRCLE_SIZE, color='black')

    for c in player_circles:
        ax.add_patch(c)
    ax.add_patch(ball_circle)

    annotations = []
    for i in range(10):
        label = str(i + 1) if i < 5 else str(i - 4)
        ann = ax.annotate(
            label,
            xy=(0, 0),
            color='white',
            ha='center',
            va='center',
            fontweight='bold',
            fontsize=8
        )
        annotations.append(ann)

    clock_info = ax.annotate(
        '',
        xy=(Constant.X_CENTER, Constant.Y_CENTER),
        color='black',
        ha='center',
        va='center',
        fontsize=10
    )

    def update(frame):
        row = df.iloc[frame]
        for i, circle in enumerate(player_circles):
            x = row[f'player_{i + 1}_x']
            y = row[f'player_{i + 1}_y']
            circle.center = (x, y)
            annotations[i].set_position((x, y))

        bx = row['ball_x']
        by = row['ball_y']
        br = row['ball_radius']
        ball_circle.center = (bx, by)
        ball_circle.set_radius(br * 0.2)

        pos_clock = row['possession_clock']
        clock_info.set_text(f"{pos_clock:.2f}s")

    anim = animation.FuncAnimation(
        fig,
        update,
        frames=len(df),
        interval=Constant.INTERVAL,
        repeat=False
    )

    writer = PillowWriter(fps=25)
    anim.save(output_path, writer=writer, dpi=80)
    plt.close(fig)
    print(f"Animación guardada: {output_path}")


GAME_NAME = input("Código de partido: ")
POSESIONES_FOLDER = f"../data/csv_posesiones/{GAME_NAME}"
OUTPUT_FOLDER = f"../../server_flask/static/gifs_posesiones/{GAME_NAME}"

if os.path.exists(OUTPUT_FOLDER):
    shutil.rmtree(OUTPUT_FOLDER)
os.makedirs(OUTPUT_FOLDER)

for file in os.listdir(POSESIONES_FOLDER):
    file_path = os.path.join(POSESIONES_FOLDER, file)

    print("Guardando Animación:", file_path)
    df = pd.read_csv(file_path)
    gif_name = os.path.splitext(file)[0] + ".gif"
    gif_path = os.path.join(OUTPUT_FOLDER, gif_name)
    create_animation(df, gif_path)
