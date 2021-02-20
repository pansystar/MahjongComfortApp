import pyscreenshot as ImageGrab
import pygetwindow as gw
import time
import io
import ctypes
import cv2
import numpy as np
from pywinauto import Desktop, Application
from pywinauto.win32structures import RECT
import MahjongSoul

class Setting:

    def __init__(self):
        # フルスクリーンではすべてを0にする
        self.frame = [112, -8, -8, 8] # Google Chrome Bookmarkバーあり

class MahjongSoul:
    # ウィンドウのキャプチャを取得
    def CaptureToImage(self):
        # img = navwin.CaptureAsImage(rect=RECT(200, 36, 250, 53))
        left = 225
        top = 944
        width = 1227
        height = 122
        item_count = 13
        item_width = float(width) / item_count
        result = list()
        for num in range(item_count):
            rect = RECT(
                self.rectMaster.left + self.setting.frame[3] + self.left_margin + int((left + (item_width * num)) * self.per)
                , self.rectMaster.top + self.setting.frame[0] + self.top_margin + int(top * self.per)
                , self.rectMaster.left + self.setting.frame[3] + self.left_margin + int((left + (item_width * num)) * self.per) + int(item_width * self.per)
                , self.rectMaster.top + self.setting.frame[0] + self.top_margin + int(top * self.per) + int(height * self.per))

            img = self.navwin.capture_as_image(rect=rect)
            # img.save(str(num) + ".png")
            result.append(img)

        return result
    # ウィンドウサイズをリフレッシュする
    def RefreshWindowSize(self):
        setting = Setting()

        self.setting = setting
        # img = navwin.CaptureAsImage(rect=RECT(200, 36, 250, 53))
        # windowサイズを取得
        rect = self.navwin.rectangle() 
        self.rectMaster = self.navwin.rectangle() 
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
        rect = self.navwin.rectangle() 
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

    def Click(self, x, y):    
        ctypes.windll.user32.SendMessageW(self.handle, 0x0201, 1, MAKELPARAM(x, y))
        ctypes.windll.user32.SendMessageW(self.handle, 0x0202, 0, MAKELPARAM(x, y))

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
        # ctypes.windll.user32.SendMessageW(self.handle, 0x0203, 0, MAKELPARAM(click_x, click_y))
        self.Click(click_x, click_y)
        self.Click(click_x, click_y)
    def ClickBrank(self):
        self.DoubleClick(258 + (-1 * 96), 992)

    def CutTehai(self,index):
        # 一番左が0, 右が12
        x = 258 + (index * 96)
        y = 992
        self.DoubleClick(x, y)
        time.sleep(0.25)
        self.ClickBrank()
    # ツモ切り
    def CutTheTsumo(self):
        # 1920x1080時の座標
        x = [1525, 1250, 960, 678, 400]
        y = 992

        for i in range(5):
            self.DoubleClick(x[i], y)
            time.sleep(0.25)

        self.ClickBrank()
    
    def Skip(self):
        # 1920x1080時の座標
        x = 1312
        y = 833

        self.Click(x, y)
        
        time.sleep(0.25)

    def Chi(self):
        # 1920x1080時の座標
        x = 1037
        y = 833

        self.Click(x, y)
        
        time.sleep(0.25)

    def Pon(self):
        # 1920x1080時の座標
        x = 1037
        y = 833

        self.Click(x, y)

        time.sleep(0.25)

# Utilityのメソッド
def MAKELPARAM(p, p_2):
    return ((p_2 << 16) | (p & 0xFFFF))
