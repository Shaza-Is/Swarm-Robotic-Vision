# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
b1Lower = (117, 10, 10)
b1Upper = (122, 255, 255)
y2Lower = (25, 10, 10)
y2Upper = (35, 255, 255)
s2Lower = (87, 10, 10)
s2Upper = (92, 255, 255)
pts_b = deque(maxlen=args["buffer"])
pts_y = deque(maxlen=args["buffer"])
pts_s = deque(maxlen=args["buffer"])
 
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)
 
# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()
 
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break
 
	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask_b = cv2.inRange(hsv, b1Lower, b1Upper) 
	mask_b = cv2.erode(mask_b, None, iterations=2)
	mask_b = cv2.dilate(mask_b, None, iterations=2)
	###########
	mask_y = cv2.inRange(hsv, y2Lower, y2Upper) 
	mask_y = cv2.erode(mask_y, None, iterations=2)
	mask_y = cv2.dilate(mask_y, None, iterations=2)
	###########
	mask_s = cv2.inRange(hsv, s2Lower, s2Upper) 
	mask_s = cv2.erode(mask_s, None, iterations=2)
	mask_s = cv2.dilate(mask_s, None, iterations=2)
	# find contours in the mask and initialize the current
	# (x, y) center of the robot
	cnts_b = cv2.findContours(mask_b.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center_b = None
	cnts_y = cv2.findContours(mask_y.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center_y = None
	cnts_s = cv2.findContours(mask_s.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center_s = None
 
	# only proceed if at least one contour was found
	if len(cnts_b) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c_b = max(cnts_b, key=cv2.contourArea)
		((x_b, y_b), radius_b) = cv2.minEnclosingCircle(c_b)
		M_b = cv2.moments(c_b)
		center_b = (int(M_b["m10"] / M_b["m00"]), int(M_b["m01"] / M_b["m00"]))
 
		# only proceed if the radius meets a minimum size
		#if radius_b > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			#cv2.circle(frame, (int(x_b), int(y_b)), int(radius_b),
			#	(0, 255, 255), 2)
			#cv2.circle(frame, center_b, 5, (0, 0, 255), -1)
 
	# update the points queue
	pts_b.appendleft(center_b)
	# loop over the set of tracked points
	for i in xrange(1, len(pts_b)):
		# if either of the tracked points are None, ignore
		# them
		if pts_b[i - 1] is None or pts_b[i] is None:
			continue
 
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 0.5)
		cv2.line(frame, pts_b[i - 1], pts_b[i], (0, 0, 255), thickness)
############################################333
# only proceed if at least one contour was found
	if len(cnts_y) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c_y = max(cnts_y, key=cv2.contourArea)
		((x_y, y_y), radius_y) = cv2.minEnclosingCircle(c_y)
		M_y = cv2.moments(c_y)
		center_y = (int(M_y["m10"] / M_y["m00"]), int(M_y["m01"] / M_y["m00"]))
 
		# only proceed if the radius meets a minimum size
		#if radius_y > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			#cv2.circle(frame, (int(x_y), int(y_y)), int(radius_y),
			#	(0, 255, 255), 2)
			#cv2.circle(frame, center_y, 5, (0, 0, 255), -1)
 
	# update the points queue
	pts_y.appendleft(center_y)
	# loop over the set of tracked points
	for i in xrange(1, len(pts_y)):
		# if either of the tracked points are None, ignore
		# them
		if pts_y[i - 1] is None or pts_y[i] is None:
			continue
 
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 0.5)
		cv2.line(frame, pts_y[i - 1], pts_y[i], (0, 255, 0), thickness)
##########################################################33
# only proceed if at least one contour was found
	if len(cnts_s) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c_s = max(cnts_s, key=cv2.contourArea)
		((x_s, y_s), radius_s) = cv2.minEnclosingCircle(c_s)
		M_s = cv2.moments(c_s)
		center_s = (int(M_s["m10"] / M_s["m00"]), int(M_s["m01"] / M_s["m00"]))
 
		# only proceed if the radius meets a minimum size
		#if radius_s > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			#cv2.circle(frame, (int(x_s), int(y_s)), int(radius_s),
			#	(0, 255, 255), 2)
			#cv2.circle(frame, center_s, 5, (255, 0, 0), -1)
 
	# update the points queue
	pts_s.appendleft(center_s)
	# loop over the set of tracked points
	for i in xrange(1, len(pts_s)):
		# if either of the tracked points are None, ignore
		# them
		if pts_s[i - 1] is None or pts_s[i] is None:
			continue
 
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 0.5)
		cv2.line(frame, pts_s[i - 1], pts_s[i], (255, 0, 0), thickness)
 
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()