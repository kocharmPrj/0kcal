import numpy as np
import cv2
import openvino as ov
from imutils.contours import sort_contours
import imutils
from difflib import SequenceMatcher


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
        
    def MakeRoi(self, Mat):
        self.image = Mat
        if self.image is not None:
            h = np.shape(self.image)[0]
            w = np.shape(self.image)[1]
            img_resized = cv2.resize(self.image, (int(w/2), int(h/2)))
            self.frame = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(self.frame, (5, 5), 0)
            edged = cv2.Canny(blurred, 250, 250)
            
            cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            cnts = sort_contours(cnts, method='left-to-right')[0]
            x_min = np.shape(img_resized)[1]
            for c in cnts:
                (x, y, w, h) = cv2.boundingRect(c)
                if w*h>100 and w*h < 150:
                    if x < x_min:
                        x_min = x
            for c in cnts:
                (x, y, w, h) = cv2.boundingRect(c)
                if w*h>70 and w*h < 150:
                    if x < x_min + 5:
                        self.width = w
                        self.height = h
                        self.point.append([x, y])
        
    def Inference(self, Mat):
        core = ov.Core()
        model = core.read_model(self.model_path)
        ppp = ov.preprocess.PrePostProcessor(model)
        self.image = Mat
        point_size = len(self.point)
        result_string = []
        for i in range(point_size):
            x = self.point[i][0]
            y = self.point[i][1]
            text = True
            t_list = []
            while text is True:
                roi = self.frame[y-7:y + self.height + 7, x - 3:x + self.width + 3]
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
                if probs[max_index] < 2:
                    text = False
                    break
                t_list.append(temp)
                x = x + self.width + 6
            temp_string = ''.join(t_list)
            result_string.append(temp_string)
        return result_string


def main():
    image_path = '/home/kimjinho/Downloads/0kcal-menu5.png'
    model_path = '/home/kimjinho/ai-project/test_models/ta-mobile3/openvino.xml'

    # Read the image using OpenCV
    image = cv2.imread(image_path)

    # Create an instance of MenuProcessor
    menu_processor = MenuProcessor(image, model_path)

    # Call the MakeRoi method to identify regions of interest
    menu_processor.MakeRoi(image)

    # Call the Inference method to perform OCR on identified regions
    result_strings = menu_processor.Inference(image)

    # Display the result strings
    print("Menu Lists:")
    for i, result_string in enumerate(result_strings):
        print(f"Menu {i + 1}: {result_string}")



if __name__ == "__main__":
    main()