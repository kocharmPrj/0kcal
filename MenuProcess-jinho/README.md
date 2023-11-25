# Text Classification
Text 분류모델 training 결과

## Dataset
Each alphabet(a~z) 500, total 13,000.

### Add font data
사용할 폰트 데이터 100개씩 추가 (a~z)

### Full data
다운로드 받은 a~z data 전부 사용 총 ( 213,848개)

## Training 결과
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

## 사용 모델 선정
Dataset Full data
모델 MobileNet-V3-large-1x
Batch_size 32, Epoch 14 

### 선정 이유
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