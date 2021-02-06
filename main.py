import pyscreenshot as ImageGrab
import pygetwindow as gw
import io
import ctypes
import cv2
import numpy as np
from pywinauto import Desktop, Application
from pywinauto.win32structures import RECT

class Setting:

    def __init__(self):
        self.frame = [112, -8, -8, 8]

class MahjongSoul:

    def CaptureToImage():
        return 0

    def RefreshWindowSize():        
        return 0
    
    def __init__(self, handle):
        self.handle = handle
        self.app = Application().connect(handle=handle)
        self.navwin = self.app.window(handle=handle)
        self.w_aspect = 16
        self.h_aspect = 9


def MAKELPARAM(p, p_2):
    return ((p_2 << 16) | (p & 0xFFFF))


setting = Setting()

# イメージインスタンス
img = ImageGrab.grab()

# データをバッファに格納
buffer = io.BytesIO()
img.save(buffer, "BMP")

titles = gw.getAllTitles()
handle = None

for item in titles:
    if("雀魂" in item):
        handle = ctypes.windll.user32.FindWindowW(0, item)
        break

if(handle != None):
    game = MahjongSoul(handle)

    app = Application().connect(handle=handle)
    navwin = app.window(handle=handle)
    # img = navwin.CaptureAsImage(rect=RECT(200, 36, 250, 53))
    rect = navwin.Rectangle() 
    img = navwin.CaptureAsImage()

    rect.top = rect.top + setting.frame[0]
    rect.right = rect.right + setting.frame[1]
    rect.bottom = rect.bottom +setting.frame[2]
    rect.left = rect.left +setting.frame[3]

    # 
    w = rect.right - rect.left
    h = rect.bottom - rect.top

    # アスペクト比で割ったチャンクごとのサイズを取得
    w_item = w / game.w_aspect 
    h_item = h / game.h_aspect

    # 黒余白部を削除し
    # ゲームウィンドウサイズを取得
    if(w_item < h_item):
        h_temp = (h - w_item * game.h_aspect) / 2
        rect.top = int(rect.top + h_temp)
        rect.bottom = int(rect.bottom - h_temp)
    else:
        w_temp = (w - h_item * game.w_aspect ) / 2
        rect.left = int(rect.left + w_temp)
        rect.right = int(rect.right - w_temp)

    navwin.CaptureAsImage(rect).save("resize.png")
    
    img.save(buffer, "BMP")

    # 画像出力
    with open("img2.bmp", "wb") as filewrite:
        filewrite.write(buffer.getvalue())

    ctypes.windll.user32.SendMessageW(handle, 0x0201, 1, MAKELPARAM(292, 145))
    ctypes.windll.user32.SendMessageW(handle, 0x0202, 0, MAKELPARAM(292, 145))

    print(handle)

