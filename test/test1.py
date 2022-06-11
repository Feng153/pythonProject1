import cv2
import datetime

img = cv2.imread('../img/img.png')
time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
cv2.imwrite('../img/img-' + str(time) + '.jpg', img)
