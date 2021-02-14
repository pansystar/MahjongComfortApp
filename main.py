import pyscreenshot as ImageGrab
import pygetwindow as gw
import time
import io
import socket
import ctypes
import cv2
import numpy as np
from pywinauto import Desktop, Application
from pywinauto.win32structures import RECT
from MahjongSoul import *
from MahjongSoulImage.itemControl import *
from Julius import *


itemControl = ItemControl()

# template = cv2.imread("template1.png", 0)

# イメージインスタンス
# img = ImageGrab.grab()

# データをバッファに格納
# buffer = io.BytesIO()
# img.save(buffer, "BMP")

titles = gw.getAllTitles()
handle = None

## 雀魂を探す
for item in titles:
    if("雀魂" in item):
        handle = ctypes.windll.user32.FindWindowW(0, item)
        break

# 雀魂が見つかったとき
if(handle != None):
    game = MahjongSoul(handle)
    julius = Julius()
    hai_list = list()

    special_command_dict = {
        "ツモ切り": game.CutTheTsumo,
        "スキップ": game.Skip,
        "チー": game.Chi,
        "ポン": game.Pon,
        "ロン": game.Pon,
        "ツモ": game.Pon,
        "立直": game.Pon,
    }

    while True:
        try:
            hai_list.clear()
            time.sleep(1.0)
            game.Update()
            julius.Update()
                
            if julius.text != "":

                if julius.text in special_command_dict:
                    special_command_dict[julius.text]()
                else:
                    img_list = game.CaptureToImage()
                    
                    for item in img_list:
                        # イメージインスタンス
                        img = np.asarray(item)
                        # データをバッファに格納
                        result = itemControl.analyze(img)
                        hai_list.append(result)

                    for i in range(len(hai_list)):
                        if hai_list[i].name == julius.text:
                            game.CutTehai(i)
                    
                julius.text = ""

                
                # if "ツモ切り" == julius.text:
                #     game.CutTheTsumo()
                # if "スキップ" == julius.text:
                #     game.Skip()
                # if "チー" == julius.text:
                #     game.Chi()
                # if "ポン" == julius.text:
                #     game.Pon()
                # if "ロン" == julius.text:
                #     game.Pon()
                # if "ツモ" == julius.text:
                #     game.Pon()
                # if "立直" == julius.text:
                #     game.Pon()
        except:
            julius.text = ""
        
else:
    print("雀魂が見つからなかったため、終了します。")
