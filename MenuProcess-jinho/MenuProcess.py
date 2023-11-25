import numpy as np
import cv2
import openvino as ov
from imutils.contours import sort_contours
import imutils


class MenuProcessor:
    def __init__(self, Mat, model_path):
        self.image = Mat
        self.model_path = model_path
        self.point = []
        self.width = 0
        self.height = 0
        self.frame = Mat
        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.ppp_flag = True
        
    def reorder(self, myPoints):
        myPoints = myPoints.reshape((4, 2))
        myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
        add = myPoints.sum(1)

        myPointsNew[0] = myPoints[np.argmin(add)]
        myPointsNew[3] = myPoints[np.argmax(add)]
        diff = np.diff(myPoints, axis=1)
        myPointsNew[1] = myPoints[np.argmin(diff)]
        myPointsNew[2] = myPoints[np.argmax(diff)]

        return myPointsNew
    
    def biggestContour(self, contours):
        biggest = np.array([])
        max_area = 0
        for i in contours:
            area = cv2.contourArea(i)
            if area > 5000:
                peri = cv2.arcLength(i, True)
                approx = cv2.approxPolyDP(i, 0.02 * peri, True)
                if area > max_area and len(approx) == 4:
                    biggest = approx
                    max_area = area
        return biggest, max_area
    
    def scanDocumentsInImage(self, inputImage):
        heightImg = 659
        widthImg = 668
        inputImage = cv2.resize(inputImage, (widthImg, heightImg))
        imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8)
        imgGray = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)  # ADD GAUSSIAN BLUR
        thres = [200, 255]
        imgThreshold = cv2.Canny(imgBlur, thres[0], thres[1])  # APPLY CANNY BLUR
        kernel = np.ones((5, 5))
        imgDial = cv2.dilate(imgThreshold, kernel, iterations=2)  # APPLY DILATION
        imgThreshold = cv2.erode(imgDial, kernel, iterations=1)  # APPLY EROSION

        # FIND ALL COUNTOURS
        imgContours = inputImage.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
        contours, hierarchy = cv2.findContours(
            imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # FIND ALL CONTOURS
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10)  # DRAW ALL DETECTED CONTOURS

        # FIND THE BIGGEST COUNTOUR
        biggest, maxArea = self.biggestContour(contours)  # FIND THE BIGGEST CONTOUR
        if biggest.size != 0:
            biggest = self.reorder(biggest)
            # DRAW THE BIGGEST CONTOUR
            pts1 = np.float32(biggest)  # PREPARE POINTS FOR WARP
            pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])  # PREPARE POINTS FOR WARP
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            imgWarpColored = cv2.warpPerspective(inputImage, matrix, (widthImg, heightImg))

            # REMOVE 20 PIXELS FORM EACH SIDE
            imgWarpColored = imgWarpColored[20:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 20]
            imgWarpColored = cv2.resize(imgWarpColored, (widthImg, heightImg))

            # APPLY ADAPTIVE THRESHOLD
            imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
            imgAdaptiveThre = cv2.adaptiveThreshold(imgWarpGray, 255, 1, 1, 7, 2)
            imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
            imgAdaptiveThre = cv2.medianBlur(imgAdaptiveThre, 3)

            return imgWarpColored
        else:
            return imgBlank

    def MakeRoi(self, mat):
        self.image = mat
        if self.image is not None:
            #h = np.shape(self.image)[0]
            #w = np.shape(self.image)[1]
            #img_resized = cv2.resize(self.image, (int(w/2), int(h/2)))
            self.frame = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(self.frame, (5, 5), 0)
            edged = cv2.Canny(blurred, 190, 210)

            cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            cnts = sort_contours(cnts, method='left-to-right')[0]
            x_min = np.shape(self.image)[1]
            for c in cnts:
                (x, y, w, h) = cv2.boundingRect(c)
                if w*h > 90 and w*h < 150:
                    if x < x_min:
                        x_min = x
            for c in cnts:
                (x, y, w, h) = cv2.boundingRect(c)
                if w*h > 80 and w*h < 150:
                    if x < x_min + 5:
                        self.width = w
                        self.height = h
                        self.point.append([x, y])

    def Inference(self, mat):
        core = ov.Core()
        model = core.read_model(self.model_path)
        ppp = ov.preprocess.PrePostProcessor(model)
        self.image = mat
        point_size = len(self.point)
        result_string = []
        for i in range(point_size):
            x = self.point[i][0]
            y = self.point[i][1]
            text = True
            t_list = []
            while text is True:
                roi = self.frame[y-7:y + self.height + 7, x - 3:x + self.width + 2]
                roi_resized = cv2.resize(roi, (128, 128))
                _, roi_resized = cv2.threshold(roi_resized, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                roi_resized = cv2.cvtColor(roi_resized, cv2.COLOR_GRAY2BGR)
                input_tensor = np.expand_dims(roi_resized, 0)
                if self.ppp_flag is True:
                    _, h, w, _ = input_tensor.shape
                    ppp.input().tensor() \
                        .set_shape(input_tensor.shape) \
                        .set_element_type(ov.Type.u8) \
                        .set_layout(ov.Layout('NHWC'))
                    ppp.input().preprocess() \
                        .resize(ov.preprocess.ResizeAlgorithm.RESIZE_LINEAR)
                    ppp.input().model().set_layout(ov.Layout('NCHW'))
                    ppp.output().tensor().set_element_type(ov.Type.f32)
                    model = ppp.build()
                    device_name = 'CPU'
                    compiled_model = core.compile_model(model, device_name)
                    self.ppp_flag = False
                results = compiled_model.infer_new_request({0: input_tensor})
                predictions = next(iter(results.values()))
                probs = predictions.reshape(-1)
                max_index = np.argmax(probs)
                temp = self.alphabet[max_index]
                if probs[max_index] < 3:
                    text = False
                    break
                t_list.append(temp)
                x = x + self.width + 6
            temp_string = ''.join(t_list)
            result_string.append(temp_string)
        return result_string


def main():
    image_path = '/home/kimjinho/ai-project/new-menu1.png'
    model_path = '/home/kimjinho/ai-project/test_models/ta-mobile3/openvino.xml'
    # Read the image using OpenCV
    image = cv2.imread(image_path)
    scan = image
    # Create an instance of MenuProcessor
    menu_processor = MenuProcessor(image, model_path)

    cam = cv2.VideoCapture(0)
    while True:
        _, img = cam.read()
        if img is None:
            print("Failed to capture image from camera")
        cv2.imshow('img', img)
        scan = menu_processor.scanDocumentsInImage(img)
        cv2.imshow('scan', scan)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    scan = cv2.cvtColor(scan, cv2.COLOR_BGR2GRAY)
    sharpening_mask1 = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    scan = cv2.filter2D(scan, -1, sharpening_mask1)
    _, scan = cv2.threshold(scan, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    scan = cv2.cvtColor(scan, cv2.COLOR_GRAY2BGR)
    cv2.imshow('scan', scan)
    cv2.waitKey()
    # Call the MakeRoi method to identify regions of interest

    menu_processor.MakeRoi(scan)

    # Call the Inference method to perform OCR on identified regions
    result_strings = menu_processor.Inference(scan)

    # Display the result strings
    print("Menu Lists:")
    for i, result_string in enumerate(result_strings):
        print(f"Menu {i + 1}: {result_string}")


if __name__ == "__main__":
    main()