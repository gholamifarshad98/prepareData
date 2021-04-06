import cv2
import numpy as np
from tqdm import tqdm
import json

fileObject = open("selectedFrame.json", "r")
jsonContent = fileObject.read()
selectedList = json.loads(jsonContent)
print(selectedList)

# Termination criteria for refining the detected corners
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((7 * 4, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:4].T.reshape(-1, 2)

img_ptsL = []
img_ptsR = []
obj_pts = []

for leftFrame in tqdm(selectedList):
    imgL = cv2.imread(leftFrame)
    imgL = cv2.resize(imgL, (640, 640))
    imgR = cv2.imread(leftFrame.replace('LeftCamera', 'RightCamera'))
    imgR = cv2.resize(imgR, (640, 640))
    imgL_gray = cv2.imread(leftFrame, 0)
    imgL_gray = cv2.resize(imgL_gray, (640, 640))
    imgR_gray = cv2.imread(leftFrame.replace('LeftCamera', 'RightCamera'), 0)
    imgR_gray = cv2.resize(imgR_gray, (640, 640))
    outputL = imgL.copy()
    outputR = imgR.copy()

    retR, cornersR = cv2.findChessboardCorners(outputR, (7, 4), None)
    retL, cornersL = cv2.findChessboardCorners(outputL, (7, 4), None)

    if retR and retL:
        obj_pts.append(objp)
        cv2.cornerSubPix(imgR_gray, cornersR, (11, 11), (-1, -1), criteria)
        cv2.cornerSubPix(imgL_gray, cornersL, (11, 11), (-1, -1), criteria)
        cv2.drawChessboardCorners(outputR, (7, 4), cornersR, retR)
        cv2.drawChessboardCorners(outputL, (7, 4), cornersL, retL)
        pair_chessboard = cv2.hconcat([outputL, outputR])
        cv2.imshow('corners', pair_chessboard)
        cv2.waitKey(0)
        img_ptsL.append(cornersL)
        img_ptsR.append(cornersR)



# Calibrating left camera

retL, mtxL, distL, rvecsL, tvecsL = cv2.calibrateCamera(obj_pts, img_ptsL, imgL_gray.shape[::-1], None, None)
hL, wL = imgL_gray.shape[:2]
new_mtxL, roiL = cv2.getOptimalNewCameraMatrix(mtxL, distL, (wL, hL), 1, (wL, hL))

# Calibrating right camera
retR, mtxR, distR, rvecsR, tvecsR = cv2.calibrateCamera(obj_pts, img_ptsR, imgR_gray.shape[::-1], None, None)
hR, wR = imgR_gray.shape[:2]
new_mtxR, roiR = cv2.getOptimalNewCameraMatrix(mtxR, distR, (wR, hR), 1, (wR, hR))


flags = 0
flags |= cv2.CALIB_FIX_INTRINSIC
# Here we fix the intrinsic camara matrixes so that only Rot, Trns, Emat and Fmat are calculated.
# Hence intrinsic parameters are the same
criteria_stereo= (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# This step is performed to transformation between the two cameras and calculate Essential and Fundamenatl matrix
retS, new_mtxL, distL, new_mtxR, distR, Rot, Trns, Emat, Fmat = cv2.stereoCalibrate(obj_pts, img_ptsL, img_ptsR, new_mtxL, distL, new_mtxR, distR, imgL_gray.shape[::-1], criteria_stereo, flags)



rectify_scale= 1
rect_l, rect_r, proj_mat_l, proj_mat_r, Q, roiL, roiR= cv2.stereoRectify(new_mtxL, distL, new_mtxR, distR, imgL_gray.shape[::-1], Rot, Trns, rectify_scale,(0,0))



Left_Stereo_Map= cv2.initUndistortRectifyMap(new_mtxL, distL, rect_l, proj_mat_l,
                                             imgL_gray.shape[::-1], cv2.CV_16SC2)
Right_Stereo_Map= cv2.initUndistortRectifyMap(new_mtxR, distR, rect_r, proj_mat_r,
                                              imgR_gray.shape[::-1], cv2.CV_16SC2)

print("Saving paraeters ......")
print(type(Right_Stereo_Map[0]))
cv_file = cv2.FileStorage("improved_params2.xml", cv2.FILE_STORAGE_WRITE)
cv_file.write("Left_Stereo_Map_x",Left_Stereo_Map[0])
cv_file.write("Left_Stereo_Map_y",Left_Stereo_Map[1])
cv_file.write("Right_Stereo_Map_x",Right_Stereo_Map[0])
cv_file.write("Right_Stereo_Map_y",Right_Stereo_Map[1])
cv_file.release()









pair_befor = cv2.hconcat([imgL, imgR])
Left_nice= cv2.remap(imgL,Left_Stereo_Map[0],Left_Stereo_Map[1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
Right_nice= cv2.remap(imgR,Right_Stereo_Map[0],Right_Stereo_Map[1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
Left_nice_gray = cv2.cvtColor(Left_nice, cv2.COLOR_BGR2GRAY)
Right_nice_gray = cv2.cvtColor(Right_nice, cv2.COLOR_BGR2GRAY)
pair_after = cv2.hconcat([Left_nice, Right_nice])
cv2.imshow("before rectification", pair_befor)
cv2.imshow("after rectification", pair_after)
cv2.waitKey(0)

out = Right_nice.copy()
out[:,:,0] = Right_nice[:,:,0]
out[:,:,1] = Right_nice[:,:,1]
out[:,:,2] = Left_nice[:,:,2]

cv2.imshow("Output image", out)
cv2.waitKey(0)


from matplotlib import pyplot as plt

stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
disparity = stereo.compute(Left_nice_gray,Right_nice_gray)
plt.imshow(disparity,'gray')
plt.show()
