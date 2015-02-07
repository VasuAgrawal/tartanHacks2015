import cv2
import numpy as np
import tesseract

testImage = cv2.imread('someGirl.jpg')

for i in xrange(len(testImage)):
    for j in xrange(len(testImage[i])):
        change = True
        for k in xrange(len(testImage[i][j])):
            if abs(testImage[i][j][k] - 255) > 10:
                change = False
        if change:
            for k in xrange(len(testImage[i][j])):
                testImage[i][j][k] = 0
        else:
            for k in xrange(len(testImage[i][j])):
                testImage[i][j][k] = 255

cv2.imshow("title", testImage)

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

api = tesseract.TessBaseAPI()
api.Init(".", "eng", tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_AUTO)

print "Starting to detect!"
tesseract.SetCvImage(testImage, api)
print api.GetUTF8Text()
print
print "Confidence:", api.MeanTextConf()

api.End()