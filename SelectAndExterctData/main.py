import os
import json
import cv2


def extract_data(video_path, initial_frame_number, extract_step):
    initial_frame = int(initial_frame_number)
    result_dir = os.path.splitext(video_path)[0]
    print(result_dir)
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    cap = cv2.VideoCapture(video_path)
    frame_counter = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        correct_frame_number = frame_counter - int(initial_frame)
        if correct_frame_number % extract_step == 0:
            temp_name = str(int(correct_frame_number / extract_step)) + '.png'
            file_address = os.path.join(result_dir, temp_name)
            cv2.imwrite(file_address, frame)
        frame_counter += 1
    cap.release()


file_name = '../SetInitialFrame/initiateFrameNumbers.json'
extractStep = 200
with open(file_name, "r") as write_file:
    data = json.load(write_file)
tempList = []
for jsonObj in data:
    extract_data(jsonObj, data[jsonObj], 75)
    print(jsonObj)
