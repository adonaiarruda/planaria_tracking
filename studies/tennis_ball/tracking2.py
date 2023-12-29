# Lets start 
import cv2, imutils
tracker = cv2.TrackerCSRT_create()
camera=True # Set it to True for webcam, else its video
if camera: 
	video  = cv2.VideoCapture(0)
else:
	video = cv2.VideoCapture('tennis_tracking.mp4')
_,frame = video.read()
frame = imutils.resize(frame,width=720)
BB = cv2.selectROI(frame,False)
tracker.init(frame, BB)
while True:
	_,frame = video.read()
	frame = imutils.resize(frame,width=720)
	track_success, BB = tracker.update(frame)
	if track_success:
		top_left = (int(BB[0]),int(BB[1]))
		bottom_right = (int(BB[0]+BB[2]), int(BB[1]+BB[3]))
		cv2.rectangle(frame,top_left,bottom_right,(0,255,0),5)
	cv2.imshow('Output',frame)
	key  =  cv2.waitKey(1) & 0xff
	if key == ord('q'):
		break
video.release()
cv2.destroyAllWindows()