import cv2
import cv2.cv as cv
import numpy as np
import tesseract

class TextDetector(object):
    def __init__(self):
        self.original = None
        self.manipulate = None
        self.tol = 50
        self.colorMax = 255
        self.white = np.array([255, 255, 255], dtype = np.uint8)
        self.black = np.array([0, 0, 0], dtype = np.uint8)
        self.kernel = np.ones((3,3), dtype = np.uint8)
        self.tessApi = tesseract.TessBaseAPI()
        self.tessApi.Init(".", "eng", tesseract.OEM_DEFAULT)
        self.tessApi.SetPageSegMode(tesseract.PSM_AUTO)
        self.text = []
        self.minConfidence = 0
        self.joinedText = ""
        self.commandCode = "##"

    def thresholdImage(self):
        self.manipulate = np.copy(self.original)
        for i in xrange(len(self.manipulate)):
            for j in xrange(len(self.manipulate[i])):
                isWhite = True
                for k in xrange(len(self.manipulate[i][j])):
                    if abs(self.original[i][j][k] - self.colorMax) > self.tol:
                        isWhite = False
                if isWhite:
                    self.manipulate[i][j] = self.white
                else:
                    self.manipulate[i][j] = self.black

    def dilateImage(self):
        self.manipulate = cv2.dilate(self.manipulate, self.kernel, iterations = 1)

    # https://code.google.com/p/python-tesseract/
    def ocr(self):
        height, width, channel = self.manipulate.shape
        iplimage = cv.CreateImageHeader((width, height), cv.IPL_DEPTH_8U, channel)
        cv.SetData(iplimage, self.manipulate.tostring(), self.manipulate.dtype.itemsize * channel * (width))
        tesseract.SetCvImage(iplimage, self.tessApi)
        self.tessApi.Recognize(None)
        ri = self.tessApi.GetIterator()
        level = tesseract.RIL_WORD
        
        self.text = []

        while ri:
            self.text.append((ri.GetUTF8Text(level), ri.Confidence(level)))
            if not ri.Next(level):
                return

    def cleanText(self):
        for i in xrange(len(self.text) - 1, -1, -1):
            word, confidence = self.text[i]
            if confidence < self.minConfidence:
                self.text.pop(i)

    def textString(self):
        for word, confidence in self.text:
            if word != None: self.joinedText += word + " "

    def findCommands(self):
        stripped = self.joinedText[self.joinedText.find(self.commandCode):]
        split = stripped.split()
        return ("".join(split[0:1]), split[1:])

    def getText(self, identifier):
        self.original = cv2.imread("snaps/" + identifier + ".jpg")
        self.manipulate = np.copy(self.original)
        self.thresholdImage()
        self.dilateImage()
        self.ocr()
        self.cleanText()
        self.textString()
        command, params = self.findCommands()

        # cv2.imshow("Dilated", self.manipulate)

        # while True:
        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         return

        return command, params

    def close(self):
        self.tessApi.End()

# detector = TextDetector()

# print "Starting"
# print

# print detector.getText("fletch")