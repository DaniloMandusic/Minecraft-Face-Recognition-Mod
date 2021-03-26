import cv2 as cv
import numpy as np

class Vision:

    # properties
    objectImage = None
    weight = 0
    heght = 0
    method = None
    objectImageName = None

    def __init__(self, objectImage, method=cv.TM_CCOEFF_NORMED):

        self.objectImageName = objectImage[:-4]

        #fullImage = cv.imread('maxresdefault.jpg',cv.IMREAD_UNCHANGED)
        self.objectImage = cv.imread(objectImage,cv.IMREAD_UNCHANGED)

        #save dimensions for object image
        self.weight = self.objectImage.shape[1]
        self.heght = self.objectImage.shape[0]

        # There are 6 methods to choose from:
        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method


    def findObjects(self, fullImage, threshold = 0.5, debugMode = None):

        result = cv.matchTemplate(fullImage, self.objectImage, self.method)

        #get all positions of object
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        #group rectangles
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.weight, self.heght]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        points = []
        if len(rectangles):

            line_color = (0, 255, 0)
            line_type = cv.LINE_4
            marker_color = (255, 0, 255)
            marker_type = cv.MARKER_CROSS

            # Loop over all the rectangles
            for (x, y, w, h) in rectangles:

                # Determine the center position
                center_x = x + int(w / 2)
                center_y = y + int(h / 2)
                # Save the points
                points.append((center_x, center_y))

                if debugMode == 'rectangles':
                    # Determine the box position
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)
                    # Draw the box
                    cv.putText(fullImage,self.objectImageName,top_left, cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, 1)
                    cv.rectangle(fullImage, top_left, bottom_right, color=line_color,
                                 lineType=line_type, thickness=2)
                elif debugMode == 'points':
                    # Draw the center point
                    cv.drawMarker(fullImage, (center_x, center_y),
                                  color=marker_color, markerType=marker_type,
                                  markerSize=40, thickness=2)

        if debugMode:
            cv.imshow('Matches', fullImage)

        return points