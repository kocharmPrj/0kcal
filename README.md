# !(맛있으면 0 kcal)
음식을 인식하고 해당 음식의 영양정보와 칼로리를 보여주고 기록한다.
하루 내에 기록된 정보를 바탕으로 하루 권장 칼로리 대비 섭취 칼로리 계산을 통해 식단관리를 해준다.

## High Level Design
![image](https://github.com/kocharmPrj/0kcal/assets/97004727/084f031f-3ae7-4855-b8b6-fd5a3a737b3c)

## Clone code

```shell
mkdir 0kcal_Prj && $_
git clone https://github.com/kocharmPrj/0kcal.git
```

## Prerequite

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
opencv-python 설치 시 pyqt5와 opencv-python안에 있는 qt와 충돌 발생
```shell
cd .venv/lib/python3.10/site-packages/cv2
rm -rf qt
```

## How to run

```shell
cd ~/0kcal_Prj
source .venv/bin/activate

cd ~/0kcal_Prj/0kcal/PyQt_0kcal
python Controller.py
```

## Output

* (프로젝트 실행 화면 캡쳐)

![./result.jpg](./result.jpg)

## Appendix

* (참고 자료 및 알아두어야할 사항들 기술)
