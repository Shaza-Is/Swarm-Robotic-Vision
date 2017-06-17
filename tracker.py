# Import the required modules
import dlib
import cv2
import skvideo.io
import argparse as ap
#import qr_read

def get_points():
	points = []
	[x1,y1,x2,w2] = raw_input("enter object location left top right bottom ").split()
	while([x1,y1,x2,w2] != ["0","0","0","0"]):
		points.append([int(x1),int(y1),int(x2),int(w2)])
		[x1,y1,x2,w2] = raw_input("enter object location left top right bottom ").split()
	return points

def run(source=0, dispLoc=False, count = 30):
	try:
		cam = skvideo.io.vreader(source)
	except:
		print("No video input found!!!")
		exit()
	frames = 0
	for img in cam:
		if frames%count == 0:
			if frames > 0:
				if points:
					for t in tracker:
						rect = t.get_position()
						print rect.left(), rect.top(), rect.right(), rect.bottom()
			points = get_points()
			if not points:
				print "No object to be tracked."
				frames += 1
				continue
		print frames
		frames += 1
		print len(points)

		# Initial co-ordinates of the object to be tracked 
		# Create the tracker object
		tracker = [dlib.correlation_tracker() for _ in xrange(len(points))]
		# Provide the tracker the initial position of the object
		[tracker[i].start_track(img, dlib.rectangle(*rect)) for i, rect in enumerate(points)]
        # Read frame from device or file
        # Update the tracker  
        for i in xrange(len(tracker)):
            tracker[i].update(img)
        


if __name__ == "__main__":
    # Parse command line arguments
    parser = ap.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', "--deviceID", help="Device ID")
    group.add_argument('-v', "--videoFile", help="Path to Video File")
    parser.add_argument('-l', "--dispLoc", dest="dispLoc", action="store_true")
    args = vars(parser.parse_args())

    # Get the source of video
    if args["videoFile"]:
        source = args["videoFile"]
    else:
        source = int(args["deviceID"])
    run(source, args["dispLoc"])
