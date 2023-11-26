# This Python file uses the following encoding: utf-8
import os
import platform
import cv2
import numpy as np
import requests
import json
from difflib import SequenceMatcher
from PySide2.QtGui import QPixmap
from PySide2.QtCore import QByteArray, QBuffer, QIODevice


class Model:
    def __init__(self):
        # file ptr for save, load data
        self.f_etc = None
        self.f_img = None

    # get pix, time, foodData and store it into ./data/
    def storeFoodData(self, qPixmapData: QPixmap, timeString: str, foodData: dict) -> None:
        print(f"timeString : {timeString}")
        current_date = timeString[:4]
        try:
            current_os = platform.system()
        except Exception as e:
            print(f"i dont know your os : {e}")

        if current_os == 'Linux':
            print("<LINUX>")
            self.getFilePtr(current_date)
            if self.f_etc is not None and self.f_img is not None:

                '''
                # convert image type to Qpixmap to bin to store.
                # +qImage can be saved jpg like qImg.save("title.jpg", "JPG")
                tmpQImg = QPixmap.toImage(qPixmapData)
                tmpByteArr = QByteArray()
                tmpBuffer = QBuffer(tmpByteArr)
                tmpBuffer.open(QIODevice.WriteOnly)
                tmpQImg.save(tmpBuffer, "PNG")
                # get binary data from the buffer
                binImg = tmpBuffer.data()
                # print(binImg)
                '''
                binImg = cv2.imencode('.jpg', qPixmapData)[1].tobytes()

                # write data into f
                self.f_etc.write(timeString)
                self.f_etc.write(' ')
                for i in foodData:
                    self.f_etc.writelines(str(i))
                    self.f_etc.write(' ')
                self.f_etc.write('\n')
                self.f_etc.close()

                bufSizeForImgWrite = 1024
                imgSize = len(binImg)
                bytesWritten = 0
                while bytesWritten < imgSize:
                    tmpBufForImgWrite = binImg[bytesWritten:bytesWritten+bufSizeForImgWrite]
                    # print(str(tmpBufForImgWrite))
                    print("try write")
                    print(str(self.f_img))
                    try:
                        self.f_img.write(tmpBufForImgWrite)
                    except Exception as e:
                        print("Err", e)
                        break
                    bytesWritten += len(tmpBufForImgWrite)
                print("write end")
                self.f_img.write('\n'.encode('utf-8'))
                self.f_img.close()
            else:
                print("err in getFileptr", "i can't find f_")

    # load from the file matching name(time : MMDDHHMM)
    def loadFoodData(self, timeString) -> None:
        print(f"timeString : {timeString}")
        current_date = timeString[:4]
        try:
            current_os = platform.system()
        except Exception as e:
            print(f"i dont know your os : {e}")

        if current_os == 'Linux':
            print("<LINUX>")
            # TODO!
            # get file matching name with current_date ( MMDD )
            # I THINK this function below should be changed to get file
            # which has name starting with current_date (MMDD_img and MMDD_etc)
            self.getFilePtr(current_date)
            # WHAT?
            # this is in Assuming that getFileptr
            if self.f_etc is not None and self.f_img is not None:
                print("loadFoodData")
               # 1. read etc file
               # 2. get line ( it is a data with timestring/food_name/nutrients... )
               # 3. parsing the line by '\n'
               # 4. read img file
               # 5. get line
               # 6. read bin to
               # eg. file.readline()

    # make file or open file and naming it using date argument(MMDDHHMM)
    def getFilePtr(self, date):
        self.f_etc = None
        self.f_img = None
        folderName = './data/'
        tmpFileName = date
        fileAddr = folderName+tmpFileName
        fileAddr_etc = fileAddr+'_etc'
        fileAddr_img = fileAddr+'_img'

        # chk Existance of folder in this prj folder
        if os.path.exists(folderName) and os.path.isdir(folderName):
            pass
        else:
            os.mkdir(folderName)

        # chk Existance of file in the folder, if there isnt, make it
        if os.path.exists(fileAddr_etc) and os.path.isfile(fileAddr_img):
            self.f_etc = open(fileAddr_etc, "a")
            self.f_img = open(fileAddr_img, "ab")
        else:
            self.f_etc = open(fileAddr_etc, "w")
            self.f_img = open(fileAddr_img, "wb")

    # http request using foodName list following menu board
    def foodInfoRequest(self, foodName: str) -> list:
        foodName = self.getHighestSimilarityFoodName(foodName)
        print("foodName in foodInfoRequest Func:", foodName)
        url = 'http://124.55.13.180:5001/requestFoodData'
        data = {'foodName': foodName}
        res = requests.post(url, data=data)
        if res.status_code == 200:
            pass
        else:
            print('res failed', res.status_code)

        # this is dic type
        return res.json()

    # check similarity in food Possible and return most high similar foodName
    def getHighestSimilarityFoodName(self, foodName: str) -> str:
        highestSimilarityStr = None
        highestSimilarityScore = 0
        tupleFoodList = (
            'bread', "hamburgsteak", "cheezepizza", "bulgogipizza",
            "potatopizza", "potatopizza", "pepperonipizza", "tomatopasta",
            "creampasta", "cola", "americano", "fantaorange", "rice"
        )
        for iFoodName in tupleFoodList:
            tmpSimilarityScore = SequenceMatcher(None, foodName, iFoodName)
            tmpSimilarityScore = float(tmpSimilarityScore.ratio())
            # print(tmpSimilarityScore)
            if tmpSimilarityScore > highestSimilarityScore:
                highestSimilarityStr = iFoodName
                highestSimilarityScore = tmpSimilarityScore

        return highestSimilarityStr


