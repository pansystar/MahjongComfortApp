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
import eel

itemControl = ItemControl()

eel.init("web")
eel.start("main.html", port=8500, block=False)

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

    # 特別アクションを登録しておく
    special_command_dict = {
        "ツモ切り": game.CutTheTsumo,
        "スキップ": game.Skip,
        "チー": game.Chi,
        "ポン": game.Pon,
        "ロン": game.Pon,
        "カン": game.Pon,
        "ツモ": game.Pon,
        "立直": game.Pon,
    }

    while True:
        try:
            hai_list.clear()
            game.Update()
            julius.Update()
                
            # juliusのテキストが入っていたら、処理を行う
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

                    # 赤を捨てるときはゲーム仕様より、左側の牌を捨てる
                    if julius.text.startswith("赤"):
                        for i in range(len(hai_list)):
                            if hai_list[i].name == julius.text:
                                game.CutTehai(i)
                                break
                    else:
                        for i in range(len(hai_list) - 1, -1, -1):
                            if hai_list[i].name == julius.text:
                                game.CutTehai(i)
                                break
                    
                julius.text = ""
        except:
            julius.text = ""
        
        eel.sleep(1.0)
else:
    print("雀魂が見つからなかったため、終了します。")
