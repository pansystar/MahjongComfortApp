import pyscreenshot as ImageGrab
import pygetwindow as gw
import io

# スクショ
img = ImageGrab.grab()

# データをバッファに格納
buffer = io.BytesIO()
img.save(buffer, "BMP")

# 画像出力
with open("img.bmp", "wb") as filewrite:
    filewrite.write(buffer.getvalue())


titles = gw.getAllTitles()

for item in titles:
    if(item in "Google"):
        print(item)