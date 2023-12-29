import cv2
import numpy as np

# Parameters
feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

def optical_flow(old_frame, new_frame, old_points):
    # Compute the optical flow (i.e., the motion of features)
    new_points, status, err = cv2.calcOpticalFlowPyrLK(old_frame, new_frame, old_points, None, **lk_params)
    
    # Select the points that are successfully tracked
    valid_points = new_points[status == 1]
    old_valid_points = old_points[status == 1]
    
    # Compute the speed of each tracked object
    speeds = []
    for i in range(len(valid_points)):
        dx = valid_points[i, 0] - old_valid_points[i, 0]
        dy = valid_points[i, 1] - old_valid_points[i, 1]
        speed = np.sqrt(dx*dx + dy*dy)
        speeds.append(speed)
    
    return valid_points, speeds

# Initialize video capture
cap = cv2.VideoCapture('tennis_tracking.mp4')

# Initialize frame and old points
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

# Main loop
while cap.isOpened():
    ret, new_frame = cap.read()
    if not ret:
        break
    
    new_gray = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
    new_points, speeds = optical_flow(old_gray, new_gray, p0)
    # print(speeds)
    
    # Draw the old points in red and the new points in green
    for old_point, new_point in zip(p0, new_points):
        a, b = old_point.ravel()
        c, d = new_point.ravel()
        print(a,b,c,d)
        cv2.line(new_frame, (int(a), int(b)), (int(c), int(d)), (0, 0, 255), 2)
        cv2.circle(new_frame, (int(a), int(b)), 5, (0, 0, 255), -1)
    
    # Display the new frame with the tracked points and speed information
    for i, (speed, new_point) in enumerate(zip(speeds, new_points)):
        x, y = new_point.ravel()
        cv2.putText(new_frame, f'Object {i+1}: {speed:.2f} pixels/frame', (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.circle(new_frame, (int(x), int(y)), 5, (0, 255, 0), -1)
    
    cv2.imshow('Optical Flow', new_frame)
    
    # Update the previous frame and points
    old_gray = new_gray.copy()
    p0 = new_points.reshape(-1, 1, 2)
    
    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close all windows
cap.release()
cv2.destroyAllWindows()