import cv2
import numpy as np

testImage = cv2.imread('someGirl.jpg')

n = 2    # Number of levels of quantization

indices = np.arange(0,256)   # List of all colors 

divider = np.linspace(0,255,n+1)[1] # we get a divider

quantiz = np.int0(np.linspace(0,255,n)) # we get quantization colors

color_levels = np.clip(np.int0(indices/divider),0,n-1) # color levels 0,1,2..

palette = quantiz[color_levels] # Creating the palette

im2 = palette[testImage]  # Applying palette on image

im2 = cv2.convertScaleAbs(im2)

testImageHSV = cv2.cvtColor(testImage, cv2.COLOR_BGR2HSV)



avgByRow = []

for i in xrange(len(testImageHSV)):
    row = testImageHSV[i, :, :]
    hues = row[:, 0]
    sats = row[:, 1]
    vals = row[:, 2]
    average = (np.average(hues), np.average(sats), np.average(vals))
    avgByRow.append(average)

def roughlyEquals(something, somethingElse, epsilon = 1):
    if len(something) != len(somethingElse):
        return False
    else:
        for i in xrange(len(something)):
            if abs(something[i] - somethingElse[i]) > epsilon:
                return False
    return True

for i in xrange(len(avgByRow)):
    print i, avgByRow[i]
    if roughlyEquals(avgByRow[i], (65, 65, 120), 20):
        print i, avgByRow[i]
        cv2.line(testImageHSV, (0, i), (600, i), 0xFF0000)

cv2.imshow("title", testImageHSV)
cv2.imshow("im2", im2)

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()