# Model 성능 비교

* 데이터 2000개 ( 각 품목당 200개 )

* 품목 리스트 : 조미김, 갈비, 시금치, 잡채, 된장찌개, 밥 , 미역국, 게장, 고등어 구이, 숙주나물

|모델  epoch, batch size | Custom_object_detection_gen3_ATSS |Custom_object_detection_gen3_SSD|Custom_object_detection_gen3_YOLOX|
|:---:|:---:|:---:|:---:|
|1/16|mAP: 0.667, Preformace: 0.56|/ |/ |
|1/32|mAP: 0.357, Preformace: 0.27|/|/|
|5/32|mAP: 0.801, Preformace: 0.73|/|/|
|10/32|mAP: 0.828, Preformace: 0.76|/|/|
|20/32|mAP: 0.843, Preformace: 0.79|/|/|
|26/32|mAP: 0.845, Preformace: 0.79|mAP: 0.845, Preformace: 0.79|mAP: 0.798, Preformace: 0.79|
|34/32|/|/|mAP: 0.819, Preformace: 0.8|

mAP : 여러 클래스에 대한 평균 정밀도


|각 품목당 최대 인식률(AP)|Custom_object_detection_gen3_ATSS|Custom_object_detection_gen3_SSD|Custom_object_detection_gen3_YOLOX|
|:---:|:---:|:---:|:---:|
|조미김|0.97|0.97|0.95|
|갈비구이|0.41|0.41|0.39|
|시금치|0.63|0.63|0.64|
|잡채|1.00|1.00|0.998|
|된장찌개|0.97|0.97|0.953|
|밥|0.94|0.94|0.90|
|미역국|0.99|0.99|1.00|
|게장|0.67|0.67|0.53|
|고등어 구이|0.80|0.80|0.79|
|숙주나물|0.99|0.99|0.97|

