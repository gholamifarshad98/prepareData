import os
import json


def write_initial_frame_number(file_path, initial_frame_number):
    file_name = 'initiateFrameNumbers.json'
    if not os.path.isfile(file_name):
        print('there is not any json file to write data.')
        temp_data = dict()
        with open(file_name, "w") as write_file:
            json.dump(temp_data, write_file)

    with open(file_name, "r") as write_file:
        data = json.load(write_file)
        os.remove(file_name)

    with open(file_name, "w") as write_file:
        if initial_frame_number != -100:
            data[file_path] = initial_frame_number
        json.dump(data, write_file)
