#!/bin/bash

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

rm -rf .venv/lib/python3.10/site-packages/cv2/qt

