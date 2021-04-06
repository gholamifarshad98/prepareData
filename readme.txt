steps to use these code

1- capture film by stereo camera from chesst board and put it in folder Data\1\LeftCamera and Data\1\RightCamera
2- capture film by stereo camera from inviroment and put it in folder Data\2\LeftCamera and Data\2\RightCamera
3- run code in setInitial frame to sync vidoes by turn on and of a lamp. this initial fram number store in a json file and used later. 
4- run code in data extraction folder and select the source folder of data. 
5- after that you must run the code selectPairFrames.py in camera calibration folder. and select perfect frame that contin correct format of chest board. about 18 frame.
6- after that run stereoCalibration.py in camera calibration folder.  these code produce rotation and transletion matrixs for right and left camera. 
7- after the you must run produceRectifiedData.py in camera calibration folder. these code rectify image and solve stereo image. 
