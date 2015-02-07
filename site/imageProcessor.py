import cv2
import numpy as np

class ImageProcessor(object):
    def __init__(self):
        pass

    def readImage(self, identifier):
        return cv2.imread('snaps/' + identifier + '.jpg')

    def writeImage(self, identifier, image):
        cv2.imwrite('snaps/' + identifier + '.jpg', image)

    def addNumber(self, identifier, number):
        if number > 99:
            return False
        image = self.readImage(identifier)
        width, height, _ = image.shape
        offset = 60 # min(width / 8, height / 8)
        cv2.ellipse(image, (offset, offset), (3 * offset / 5, 3 * offset / 5), 0, 0, 360, 0x000000, -1)

        fontFace = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        thickness = 2
        text = str(number)
        size, height = cv2.getTextSize(text, fontFace, fontScale, thickness)
        textWidth, textHeight = size
        cv2.putText(image, text, (offset - (textWidth/2) , offset + (textHeight/2)), fontFace, fontScale, (255, 255, 255), thickness)
        cv2.imwrite('snaps/' + text + '.jpg', image)

    def removeRed(self, identifier):
        image = self.readImage(identifier)
        image[:, :, 2] = 0
        self.writeImage(identifier, image)

    def removeGreen(self, identifier):
        image = self.readImage(identifier)
        image[:, :, 1] = 0
        self.writeImage(identifier, image)

    def removeBlue(self, identifier):
        image = self.readImage(identifier)
        image[:, :, 0] = 0
        self.writeImage(identifier, image)

    # def showImage(self, identifier):
    #     self.removeRed(identifier)
    #     self.addNumber(identifier, 42)

    #     added = cv2.imread('snaps/' + identifier + '.jpg')
    #     cv2.imshow("Written", added)

    #     while True:
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             return

# ImageProcessor().showImage("image3")
