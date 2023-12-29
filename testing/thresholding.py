import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')




# img = cv2.imread('videos/sample.png')

# ret,thresh1 = cv2.threshold(img,210,255,cv2.THRESH_BINARY) # Threshold between values? And using colors?
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# print(gray.shape)
# ret,thresh1 = cv2.threshold(gray,210,255,cv2.THRESH_BINARY)

# Convert the array to a DataFrame
# df = pd.DataFrame(gray)

# Save the DataFrame to a CSV file
# df.to_csv('myarray.csv', index=False, header=False)


# plt.imshow(gray, interpolation='nearest')
# plt.plot(gray)
# plt.show()


# fig, ax = plt.subplots()

# min_val, max_val = 0, 255

# for i in range(235):
#     for j in range(255):
#         c = gray[i][j]
#         ax.text(i+0.5, j+0.5, str(c), va='center', ha='center')
# ax.grid()
# plt.savefig('foo.png')



cap = cv2.VideoCapture('videos/1_3NeoLOCZONA_A-96H_C0A1_P1_N1.mp4')
ret, frame1 = cap.read()
frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)


for i in range(50):
    ret, new_frame = cap.read()

ret, frame = cap.read()

frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# print(gray)
# _, threshold_img = cv2.threshold(frame, 200, 255, cv2.THRESH_BINARY)
frame = frame - frame1

cv2.imshow("bg", frame)

# Exit if 'q' is pressed
cv2.waitKey(0)