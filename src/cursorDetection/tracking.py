import numpy as np
import pyautogui as pg
import keyboard as kb
import time
import json
import threading
from keras.models import load_model
import subprocess
from sys import platform

from src.dataCollectionTool.paint.editor import process_image
from src.dataCollectionTool.paint.parameters import Parameters

directory_to_main_info = "../data/main.json"

directory_to_models_info = "../data/packs/modelsInfo"
directory_to_models = "../data/packs/models"
directory_to_symbol_info = "../data/symbols/symbolsInfo"
directory_to_scripts = "../data/scripts"

def tracking(exit_event: threading.Event):

    screen_width, screen_height = pg.size()

    image_size = {"top": screen_height, "bottom": -1, "left": screen_width, "right": -1}
    i = 0
    pos_list = []
    prev_pos = pg.position()

    while True:

        if exit_event.is_set():
            print("finished")
            return

        if kb.is_pressed('q') and kb.is_pressed('ctrl') and kb.is_pressed('shift'):
            print("finished")
            return

        if kb.is_pressed('q') and kb.is_pressed('ctrl'):

            pos = pg.position()

            if pos != prev_pos:

                pos_list.append((pos.x, pos.y, i))
                image_size = change_image_size(pos.x, pos.y, image_size)
                prev_pos = pos
                i += 1

        elif pos_list:

            execute_script(pos_list, image_size)
            image_size = restart_image_size(image_size, screen_width, screen_height)
            i = 0
            pos_list = []

        time.sleep(0.0001)


def execute_script(pos_list, image_size):

    np_img = process_image(pos_list, image_size, Parameters.RADIUS)

    if np_img is None:
        return

    with open(directory_to_main_info, "r") as file:
        selected_model = json.load(file)["selected"]

    with open(directory_to_models_info + "/" + selected_model + ".json", "r") as file:
        index_to_label = json.load(file)["index_to_label"]

    model = load_model(directory_to_models + '/' + selected_model + '.h5')

    np_img = np.expand_dims(np_img, axis=0)
    predictions = model.predict(np_img)
    predicted_symbol_number = np.argmax(predictions)

    predicted_symbol = index_to_label.get(str(predicted_symbol_number))

    print("predicted: " + predicted_symbol)

    with open(directory_to_symbol_info + "/" + predicted_symbol + ".json", "r") as file:
        selected_script = json.load(file)["script"]

    if platform == "win32":
        subprocess.run("python " + directory_to_scripts + "/" + selected_script, shell=True)

    elif platform == "darwin":
        subprocess.run("python " + directory_to_scripts + "/" + selected_script)


def change_image_size(x, y, image_size):

    if y < image_size["top"]:
        image_size["top"] = y

    if y > image_size["bottom"]:
        image_size["bottom"] = y

    if x < image_size["left"]:
        image_size["left"] = x

    if x > image_size["right"]:
        image_size["right"] = x

    return image_size


def restart_image_size(image_size, screen_width, screen_height):

    image_size["top"] = screen_height
    image_size["bottom"] = 0
    image_size["left"] = screen_width
    image_size["right"] = 0

    return image_size

