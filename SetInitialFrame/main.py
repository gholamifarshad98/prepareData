import cv2
import writeOnJsonfile

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
filePath = '../Data/RightCamera/4.mp4'
cap = cv2.VideoCapture(filePath)

# Check if camera opened successfully
if not cap.isOpened():
    print("Error opening video stream or file")
font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10, 500)
fontScale = 1
fontColor = (255, 255, 0)
lineType = 2
print(cap.get(cv2.CAP_PROP_FPS))

# Read until video is completed
frameNumber = 0
selectedFrameNumber = -100
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        cv2.putText(frame, 'Frame Number: {}'.format(frameNumber), bottomLeftCornerOfText, font, fontScale, fontColor,
                    lineType)
        # Display the resulting frame
        resizedFrame = cv2.resize(frame, (640, 640))
        cv2.imshow('Frame', resizedFrame)
        frameNumber += 1
        # Press Q on keyboard to  exit
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
        if cv2.waitKey(0) & 0xFF == ord('k'):
            selectedFrameNumber = frameNumber
            print('Frame Number: {}'.format(frameNumber))

    # Break the loop
    else:
        break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()

writeOnJsonfile.write_initial_frame_number(filePath, selectedFrameNumber)
