# !(맛있으면 0 kcal)
음식을 인식하고 해당 음식의 영양정보와 칼로리를 보여주고 기록한다.
하루 내에 기록된 정보를 바탕으로 하루 권장 칼로리 대비 섭취 칼로리 계산을 통해 식단관리를 해준다.

## High Level Design

![image](https://github.com/kocharmPrj/0kcal/assets/142784142/b029e36d-bd3c-4ac7-9c88-dde50782227c)

## Clone code

```shell
mkdir 0kcal_Prj
cd 0kcal_Prj
git clone https://github.com/kocharmPrj/0kcal.git
```

## Prerequite

```shell
cd 0kcal
./install.sh
```

install.sh

```shell
#!/bin/bash

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

rm -rf .venv/lib/python3.10/site-packages/cv2/qt
```

## How to run

```shell
./run.sh
```

run.sh

```shell
#!/bin/bash

.venv/bin/python3 ./src/Controller.py
```

## Output

![image](https://github.com/kocharmPrj/0kcal/assets/97004727/fbbd5505-a3b2-4755-b1ef-3de4344a6cfa)

![image](https://github.com/kocharmPrj/0kcal/assets/97004727/e172fa10-1717-4395-88af-b926007dd3e5)

![image](https://github.com/kocharmPrj/0kcal/assets/97004727/4a3cedc5-5a47-4437-9119-ccb6d7554717)

## Appendix
DB table 생성 및 통신 서버 구축 필요 (model.py foodInfoRequest 함수의 url 수정 필요)
* ![image](https://github.com/kocharmPrj/0kcal/assets/142784142/5690ff1e-d085-4ad7-9add-8a855c95c91d)

