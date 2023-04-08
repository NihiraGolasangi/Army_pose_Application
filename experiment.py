import cv2
import numpy as np

# open the video file
path = '/Users/atharvaparikh/Desktop/atCode/Project/DIAT/End2End Implemenations/Army_pose_Application/Testing Videos/Salute_/video_20220719_095724.mp4'
cap = cv2.VideoCapture(path)

# read the first frame of the video
ret, frame = cap.read()

# select the region of interest (ROI) by drawing a rectangle
x, y, w, h = cv2.selectROI('Frame', frame)

# close the window after ROI selection is done
cv2.destroyAllWindows()

# extract the subframe from the original frame
subframe = frame[y:y+h, x:x+w]

# create a new blank image with the same dimensions as the original frame
blank_image = np.zeros(frame.shape, np.uint8)

# insert the subframe into the blank image at the same coordinates as the ROI
blank_image[y:y+h, x:x+w] = subframe

# display the imposed frame on the new window
cv2.imshow('Imposed Frame', blank_image)

# wait for a key press
cv2.waitKey(0)

# release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()