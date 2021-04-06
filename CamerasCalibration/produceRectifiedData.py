import numpy as np
import cv2
from matplotlib import pyplot as plt

Left_Stereo_Map = []
Right_Stereo_Map = []
cv_file = cv2.FileStorage("improved_params2.xml", cv2.FILE_STORAGE_READ)
Left_Stereo_Map_x = cv_file.getNode("Left_Stereo_Map_x").mat()
Left_Stereo_Map_y = cv_file.getNode("Left_Stereo_Map_y").mat()
Right_Stereo_Map_x = cv_file.getNode("Right_Stereo_Map_x").mat()
Right_Stereo_Map_y = cv_file.getNode("Right_Stereo_Map_y").mat()
cv_file.release()
leftFrame = "../Data/LeftCamera/2/4.png"
imgL = cv2.imread(leftFrame)
imgL = cv2.resize(imgL, (640, 640))
imgR = cv2.imread(leftFrame.replace('LeftCamera', 'RightCamera'))
imgR = cv2.resize(imgR, (640, 640))
pair_before = cv2.hconcat([imgL, imgR])
Left_nice = cv2.remap(imgL,Left_Stereo_Map_x,Left_Stereo_Map_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
Right_nice = cv2.remap(imgR,Right_Stereo_Map_x,Right_Stereo_Map_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
Left_nice_gray = cv2.cvtColor(Left_nice, cv2.COLOR_BGR2GRAY)
Right_nice_gray = cv2.cvtColor(Right_nice, cv2.COLOR_BGR2GRAY)
pair_after = cv2.hconcat([Left_nice, Right_nice])
stereo = cv2.StereoBM_create(numDisparities=32, blockSize=35)
disparity = stereo.compute(Left_nice_gray,Right_nice_gray)
plt.imshow(disparity,'gray')
plt.show()
cv2.imshow("before rectification", pair_before)
cv2.imshow("after rectification", pair_after)
cv2.waitKey(0)
