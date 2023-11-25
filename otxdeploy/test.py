import cv2
import numpy as np
import openvino as ov


class ObjectDetector:
    def __init__(self, model_xml_path, model_bin_path):
        self.labels = {
            "0": { "_id": "0", "name": "seaweed", "color": (29, 232, 8, 255)},
            "1": { "_id": "1", "name": "grilled short ribs", "color": (49, 39, 11, 255)},
            "2": { "_id": "2", "name": "spinach", "color": (171, 79, 91, 255)},
            "3": { "_id": "3", "name": "japchae", "color": (38, 234, 46, 255)},
            "4": { "_id": "4", "name": "soybean paste stew", "color": (59, 136, 123, 255)},
            "5": { "_id": "5", "name": "rice", "color": (36, 68, 7, 255)},
            "6": { "_id": "6", "name": "seaweed soup", "color": (172, 27, 223, 255)},
            "7": { "_id": "7", "name": "marinated raw crabs", "color": (93, 248, 144, 255)},
            "8": { "_id": "8", "name": "grilled mackerel", "color": (189, 178, 241, 255)},
            "9": { "_id": "9", "name": "seasoned mung bean sprouts", "color": (244, 201, 238, 255)}
        }

        self.core = ov.Core()
        self.model = self.core.read_model(model=model_xml_path, weights=model_bin_path)
        self.compiled_model = self.core.compile_model(model=self.model, device_name='CPU')

        self.input_layer = self.compiled_model.input(0)
        self.output_layer_labels = self.compiled_model.output("labels")
        self.output_layer_boxes = self.compiled_model.output("boxes")

        _, _, H, W = self.input_layer.get_partial_shape()
        self.target_shape = (W.get_length(), H.get_length())

    def detect_objects(self, frame):
        resized_frame = cv2.resize(frame, self.target_shape)
        input_frame = np.expand_dims(resized_frame.transpose(2, 0, 1), axis=0)

        results = self.compiled_model([input_frame])[self.output_layer_boxes]
        class_ids = self.compiled_model([input_frame])[self.output_layer_labels]

        detected_objects = []
        label_names_list = []

        for i, detection in enumerate(results[0]):
            if np.all(detection == 0):
                continue

            x_min, y_min, x_max, y_max, score = detection
            class_id = str(class_ids[0][i])

            if score > 0.5 and class_id in self.labels:
                x_min, y_min, x_max, y_max = map(int, [x_min, y_min, x_max, y_max])
                label_name = self.labels[class_id]["name"]
                color = self.labels[class_id]["color"]
                
                label_names_list.append(label_name)
                print(" ",label_names_list)

                detected_objects.append({"label": label_name, "box": (x_min, y_min, x_max, y_max), "color": color})

        return detected_objects


if __name__ == "__main__":
    model_xml_path = "model/model.xml"
    model_bin_path = "model/model.bin"

    detector = ObjectDetector(model_xml_path, model_bin_path)

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("error : camaera no open")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("error : camaera no read")
            break

        detected_objects = detector.detect_objects(frame)

        for obj in detected_objects:
            label_name = obj["label"]
            color = obj["color"]
            x_min, y_min, x_max, y_max = obj["box"]

            # the coordinate system of yolox is different, so the box is skewed to the right, it will be fixed later
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, 2) 
            cv2.putText(frame, label_name, (x_min, y_min - 10), cv2.FONT_HERSHEY_DUPLEX, 0.9, color, 2)

        cv2.imshow("Camara", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
