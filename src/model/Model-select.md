# Object detection & Text classification

## 1. Text Classification
Text 분류모델 training 결과

### Dataset
Each alphabet(a~z) 500, total 13,000.

#### Add font data
사용할 폰트 데이터 100개씩 추가 (a~z)

#### Full data
다운로드 받은 a~z data 전부 사용 총 ( 213,848개)

### Training 결과
|Classification model|Accuracy|Batch size|epoch|기타
|----|----|----|----|----|
|DeiT-Tiny| 0.585|4|5
|DeiT-Tiny| 0.83|4|13
|DeiT-Tiny| 0.84|4|20
|DeiT-Tiny|0.94 |32| 23| add font data
|EfficientNet-V2-S| 0.82| 4|1
|EfficientNet-V2-S| 0.88| 4|5
|EfficientNet-V2-S| 0.90| 4|10
|EfficientNet-B0| 0.91 | 4| 20
|EfficientNet-B0| 0.947 | 32| 40 | add font data
|MobileNet-V3-large-1x| 0.89 | 4| 20
|MobileNet-V3-large-1x| 0.927 | 4| 25
|MobileNet-V3-large-1x| 0.94 | 16| 24 | add font data
|MobileNet-V3-large-1x| 0.93 | 32| 17 | add font data
|MobileNet-V3-large-1x| 0.948 | 8|  39| add font data
|MobileNet-V3-large-1x| 0.94 | 32|  3| full data
|MobileNet-V3-large-1x| 0.96 | 32|  14| full data

### 사용 모델 선정
Dataset Full data
모델 MobileNet-V3-large-1x
Batch_size 32, Epoch 14 

#### 선정 이유
동일 조건으로 여러 모델 train 결과 동일 조건 상에서 MobileNet 성능 우수 확인
MobileNet 으로 조건 변경해가며 train
Train 결과 인식률 부족으로 dataset(font data) 추가 후 train

결과 인식률 부족 - 이유 dataset 부족으로 판단
기존 : 다운받은 data 중 일정 개수만 사용
변경 : 다운받은 data 전부 사용(full data)
결과 : 인식률이 오르긴 했으나 충분하지 않음

해결 방안 : Inference에 사용하는 input data 전처리 알고리즘 추가
결과 : 필요 요구사항 충족

알고리즘 개선 후 기존 trained 모델 test
결과 : 마지막에 사용한 모델 성능 우수 - 해당 모델 선정

#### 성능 개선을 위한 노력
1. Dataset 문제
    다운로드 받은 데이터에서 각 알파벳 별로 500개씩의 데이터를 뽑아서 train 
    - 테스트 결과는 좋으나 실제로 사용해본 결과 인식률 낮음

    Demo에서 사용할 font로 각 알파벳 별 데이터 추가 각 99개 
    - 테스트 결과는 좋으나 실제로 사용해본 결과 인식률 낮음

    다운로드 받은 데이터 전체 사용 총 213,848개 데이터로 train
    - 테스트 결과 좋음, 실제 사용 결과 인식률 양호

2. Algorithm 개선
    인식이 안되는 이유가 inference에 사용되는 input data의 문제로 판단
    - Input image의 크기를 학습시킨 image의 크기와 일치
    - 작은 크기의 이미지를 키우는 과정에서 image 흐려짐
    - Alphabet의 윤곽이 제대로 나오도록 threshold 사용
    - 개선된 알고리즘으로 기존 trained 모델 사용 결과 인식률 안좋음

3. 유사성 검사 추가
    - Test image 파일로 검사 시 성능 우수
    - Print된 image로 검사 시 인식률 낮음
    - Test image 수정해가며 print 후 test - 인식률 증가 but 완전한 단어가 나오지 않음
    - 유사성 검사과정 추가 - 단어간 유사도를 비교 후 완전한 단어로 출력 - 결과 우수

## 2. Object Detection 성능 비교

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

