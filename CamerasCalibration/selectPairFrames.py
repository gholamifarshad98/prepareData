import cv2
import glob
import re
from tqdm import tqdm
import json
# The number of inner corners in chess board.

leftCameraDataPath = '../Data/LeftCamera/1/*.png'
leftFramesPaths = glob.glob(leftCameraDataPath)  # or (rightCameraDataPath and LeftCameraDataPath)

# Image properties
frame_width = 640
frame_height = 640
frameSize = (frame_width, frame_height)
fps = 1

# Font for write on frames.
font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10, 500)
fontScale = 1
fontColor = (255, 255, 255)
lineType = 2

rowCorners = 4
columnCorners = 7

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
selectedList = []
for leftFramePath in tqdm(leftFramesPaths):
    leftImg = cv2.imread(leftFramePath)
    leftImg = cv2.resize(leftImg, frameSize)
    leftGray = cv2.cvtColor(leftImg, cv2.COLOR_BGR2GRAY)

    rightFramePath = leftFramePath.replace('LeftCamera', 'RightCamera')
    rightImg = cv2.imread(rightFramePath)
    rightImg = cv2.resize(rightImg, frameSize)
    rightGray = cv2.cvtColor(rightImg, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    leftRet, leftCorners = cv2.findChessboardCorners(leftGray, (columnCorners, rowCorners), None)
    rightRet, rightCorners = cv2.findChessboardCorners(rightGray, (columnCorners, rowCorners), None)
    # If found, add object points, image points (after refining them)
    if leftRet and rightRet:
        corners2left = cv2.cornerSubPix(leftGray, leftCorners, (11, 11), (-1, -1), criteria)
        corners2right = cv2.cornerSubPix(rightGray, rightCorners, (11, 11), (-1, -1), criteria)
        picNumber = re.findall(r'\d+', leftFramePath)
        # Draw and display the corners
        leftImgDrawChessboard = cv2.drawChessboardCorners(leftImg, (columnCorners, rowCorners), corners2left, leftRet)
        rightImgDrawChessboard = cv2.drawChessboardCorners(rightImg, (columnCorners, rowCorners), corners2right,
                                                           rightRet)
        cv2.putText(leftImgDrawChessboard, 'frame number is: {}'.format(picNumber[1]), bottomLeftCornerOfText, font,
                    fontScale, fontColor,
                    lineType)
        cv2.putText(rightImgDrawChessboard, 'frame number is: {}'.format(picNumber[1]), bottomLeftCornerOfText, font,
                    fontScale, fontColor,
                    lineType)
        result = cv2.hconcat([leftImgDrawChessboard, rightImgDrawChessboard])
        cv2.imshow('left chest board', result)
        if cv2.waitKey(3000) == ord('a'):
            print(leftFramePath)
            selectedList.append(leftFramePath)
        else:
            continue
selectedStr = json.dumps(selectedList)
jsonFile = open("selectedFrame.json", "w")
jsonFile.write(selectedStr)
jsonFile.close()
