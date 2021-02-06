import pyscreenshot as ImageGrab
import pygetwindow as gw
import time
import io
import ctypes
import cv2
import numpy as np
from pywinauto import Desktop, Application
from pywinauto.win32structures import RECT

class Setting:

    def __init__(self):
        # フルスクリーンではすべてを0にする
        self.frame = [112, -8, -8, 8] # Google Chrome Bookmarkバーあり

class MahjongSoul:
    # ウィンドウのキャプチャを取得
    def CaptureToImage(self):
        return 0
    # ウィンドウサイズをリフレッシュする
    def RefreshWindowSize(self):
        setting = Setting()

        self.setting = setting
        # img = navwin.CaptureAsImage(rect=RECT(200, 36, 250, 53))
        # windowサイズを取得
        rect = self.navwin.Rectangle() 
        self.rectMaster = self.navwin.Rectangle() 
        # ウィンドウ枠を除去
        rect.top = rect.top + setting.frame[0]
        rect.right = rect.right + setting.frame[1]
        rect.bottom = rect.bottom + setting.frame[2]
        rect.left = rect.left + setting.frame[3]

        # 幅と高さを取得
        w = rect.right - rect.left
        h = rect.bottom - rect.top

        # アスペクト比で割ったチャンクごとのサイズを取得
        w_item = w / self.w_aspect
        h_item = h / self.h_aspect
        self.top_margin = 0
        self.left_margin = 0

        # 黒余白部を削除し
        # ゲームウィンドウサイズを取得
        if(w_item < h_item):
            h_temp = (h - w_item * self.h_aspect) / 2
            rect.top = int(rect.top + h_temp)
            rect.bottom = int(rect.bottom - h_temp)
            # 余白
            self.top_margin = h_temp
        else:
            w_temp = (w - h_item * self.w_aspect ) / 2
            rect.left = int(rect.left + w_temp)
            rect.right = int(rect.right - w_temp)
            # 余白
            self.left_margin = w_temp
        
        # 確定した幅と高さを取得
        new_w = rect.right - rect.left

        # 2Kサイズと比較した割合を保持しておく
        self.per = (new_w / 1920.0) 
        
        self.rect = rect

        return 0

    def Update(self):        
        rect = self.navwin.Rectangle() 
        if(self.rectMaster != rect):
            self.RefreshWindowSize()
        return
    def __init__(self, handle):
        self.handle = handle # ウィンドウハンドル
        self.app = Application().connect(handle=handle)
        self.navwin = self.app.window(handle=handle)
        
        self.w_aspect = 16
        self.h_aspect = 9

        self.RefreshWindowSize()

    def DoubleClick(self, x, y):        
        # 現在のウィンドウサイズに合わせて座標を調整
        x = x * self.per
        y = y * self.per

        click_x = int(self.setting.frame[3] + self.left_margin + x)
        click_y = int(self.setting.frame[0] + self.top_margin + y)

        # デバッグ
        # print(self.rect)
        # print('per = %f, x = %d, y = %d' % (self.per, click_x, click_y))
        
        ## ダブルクリックが必要
        Click(click_x, click_y)
        Click(click_x, click_y)

    def CutTehai(self,index):
        # 一番左が0, 右が12
        x = 258 + (index * 96)
        y = 992
        self.DoubleClick(x, y)

    # ツモ切り
    def CutTheTsumo(self):
        # 1920x1080時の座標
        x = 1525
        y = 992

        self.DoubleClick(x, y)

# Utilityのメソッド
def MAKELPARAM(p, p_2):
    return ((p_2 << 16) | (p & 0xFFFF))

def Click(x, y):    
    ctypes.windll.user32.SendMessageW(handle, 0x0201, 1, MAKELPARAM(x, y))
    ctypes.windll.user32.SendMessageW(handle, 0x0202, 0, MAKELPARAM(x, y))

# イメージインスタンス
img = ImageGrab.grab()

# データをバッファに格納
buffer = io.BytesIO()
# img.save(buffer, "BMP")

titles = gw.getAllTitles()
handle = None

for item in titles:
    if("雀魂" in item):
        handle = ctypes.windll.user32.FindWindowW(0, item)
        break

# 雀魂が見つかったとき
if(handle != None):

    game = MahjongSoul(handle)

    for i in range(500):
        time.sleep(0.5)
        game.Update()
else:
    print("雀魂が見つからなかったため、終了します。")
