# This Python file uses the following encoding: utf-8
import os
import glob
import platform
import cv2
import numpy as np
import requests
import json
import time
from difflib import SequenceMatcher
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QByteArray, QBuffer, QIODevice


class Model:
    def __init__(self):
        # file ptr for save, load data
        self.f_etc = None
        self.f_img = None

    # get pix, time, foodData and store it into ./data/
    def storeFoodData(self, qPixmapData: QPixmap, timeString: str, foodData: list) -> None:
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

                binImg = cv2.imencode('.jpg', qPixmapData)[1].tobytes()

                # size of binary Img
                imgSize = len(binImg)

                # write data into f
                self.f_etc.write(timeString)
                self.f_etc.write(' ')
                for j in foodData:
                    for i in j:
                        print("MODEL str(i)", str(i))
                        self.f_etc.write(str(i))
                        self.f_etc.write(' ')
                self.f_etc.write(str(imgSize))
                self.f_etc.write(' ')
                self.f_etc.write('\n')
                self.f_etc.close()

                bufSizeForImgWrite = 1024
                imgSize = len(binImg)
                print("MODEL imgSize in bin", imgSize)
                bytesWritten = 0
                while bytesWritten < imgSize:
                    tmpBufForImgWrite = binImg[bytesWritten:bytesWritten+bufSizeForImgWrite]
                    try:
                        self.f_img.write(tmpBufForImgWrite)
                    except Exception as e:
                        print("Err", e)
                        break
                    bytesWritten += len(tmpBufForImgWrite)
                print("write end")
                self.f_img.write(b'\n')
                self.f_img.close()
            else:
                print("err in getFileptr", "i can't find f_")

    # load from the file matching name(time : MMDDHHMM)
    def loadFoodData(self):
        try:
            current_os = platform.system()
        except Exception as e:
            print(f"i dont know your os : {e}")

        if current_os == 'Linux':
            print("<LINUX>")
            dayStr = time.localtime(time.time())
            dayStrTrimmed = str(dayStr.tm_mon) + str(dayStr.tm_mday)
            result = self.findFilePtr(dayStrTrimmed)
            if result is None:
                return None
            else:
                fEtc, fImg = result

            # read file (dayStr_etc in str, dayStr_img in bin)
            if fEtc is not None and fImg is not None:
                self.f_etc = []
                self.f_img = []
                lineCntEtc = 0
                lineCntImg = 0
                with open(fEtc, 'r') as readingEtc:
                    for line in readingEtc:
                        lineCntEtc = lineCntEtc + 1
                        tmp = line.split(' ')
                        self.f_etc.append(tmp)
                    print("MODEL str read", str(self.f_etc))
                with open(fImg, 'rb') as readingImg:
                    print("MODEL images_binary size when read", os.path.getsize(fImg))
                    img_bin_list = []
                    for idx in range(0, len(self.f_etc)):
                        img_bin = readingImg.read(int(self.f_etc[idx][9]))
                        img_bin_list.append(img_bin)
                        readingImg.read(1)

                    for i in img_bin_list:
                        print("MODEL bin size", len(i))
                    img_bin_list = [
                        np.asarray(bytearray(tmp_img), dtype=np.uint8) for tmp_img in img_bin_list if tmp_img
                    ]
                    for i in img_bin_list:
                        lineCntImg = lineCntImg+1
                        self.f_img.append(cv2.imdecode(i, flags=cv2.IMREAD_COLOR))
                        print("MODEL f_img type", type(self.f_img[0]))

                print("MODEL lineEtc", lineCntEtc, " lineImg", lineCntImg)
                return self.f_etc, self.f_img

    # make file or open file and naming it using date argument(MMDDHHMM)
    # used in write file
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

    # find files already existed for loading data(text, img)
    # used in before switch to DietWidget(diet_widget) from main
    def findFilePtr(self, date):
        imgFile = None
        textFile = None

        # make var having same name with target
        folderName = './data/'
        fileNameDefault = folderName + date + '_'

        # check there are 2 files (dayStr_etc, dayStr_img)
        if len(glob.glob(fileNameDefault+'*')) != 2:
            print("MODEL no data in today")
            return None

        # open files for reading data
        fileEtc = fileNameDefault + 'etc'
        fileImg = fileNameDefault + 'img'
        return fileEtc, fileImg

    # http request using foodName list following menu board
    def foodInfoRequest(self, foodName: str) -> list:
        print("MODEL original foodName :", str(foodName))
        foodName = self.getHighestSimilarityFoodName(foodName)
        print("MODEL foodName in foodInfoRequest Func:", foodName)
        url = 'http://124.55.13.180:5001/requestFoodData'
        data = {'foodName': foodName}
        res = requests.post(url, data=data)
        if res.status_code == 200:
            pass
        else:
            print('res failed', res.status_code)

        # this is dic type
        return res.json()

    # check similarity with food list Possible
    # and Return most high similar foodName
    def getHighestSimilarityFoodName(self, foodName: str) -> str:
        highestSimilarityStr = None
        highestSimilarityScore = 0
        tupleFoodList = (
            'bread', "hamburgsteak", "cheezepizza", "bulgogipizza",
            "potatopizza", "potatopizza", "pepperonipizza", "tomatopasta",
            "creampasta", "cola", "americano", "fantaorange", "rice",
            "soybean paste stew", "seaweed soup", "seaweed", "spinach",
            "marinated raw crabs", "japchae", "grilled short ribs",
            "grilled mackerel", "sessoned mung bean sprouts"
        )
        for iFoodName in tupleFoodList:
            tmpSimilarityScore = SequenceMatcher(None, foodName, iFoodName)
            tmpSimilarityScore = float(tmpSimilarityScore.ratio())
            # print(tmpSimilarityScore)
            if tmpSimilarityScore > highestSimilarityScore:
                highestSimilarityStr = iFoodName
                highestSimilarityScore = tmpSimilarityScore

        return highestSimilarityStr


