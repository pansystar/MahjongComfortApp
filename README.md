# MahjongComfortApp

## はじめに

## 動作確認済環境
- OS : Windows 10 Pro
- CPU : Ryzen 7 3700X
- GPU : NVIDIA GeFOrce RTX 2060 SUPER
- MIC : SHURE mv7


## 準備
本アプリケーションは、外部ツールを駆使して作動する構造となっています。必要なソフトの導入手順を以下に記します。※すべて無料です。

### Python
本アプリケーションは、Python言語で書かれているため、Pythonをインストールしておく必要があります。
下記URLから、ダウンロード&インストールしてください。
[Python Downloads](https://www.python.org/downloads/)

インストールが完了したら、コマンドプロンプトを開き、以下のコマンドを入力して、Pythonのバージョンが表示されることを確認してください。

```cmd:例
python --version
Python 3.8.2
```

### OpenCV
本アプリの画像認識で利用します。以下のコマンドを入力し、実行してください。
```cmd:例
python -m pip install opencv-python
```

### Julius
本アプリの音声認識で利用します。以下のリンクに飛び、Juliusをdownloadしてください
[Julius Releases](https://github.com/julius-speech/julius/releases)
ダウンロードしたzip内にあるフォルダを、Cドライブ直下に置いてもらい、フォルダ名を「Julius」に変更してください

また、dictation-kitもダウンロードする必要があります。以下のリンクからダウンロードしてください。(約500MB)
※サイズが大きいため、代替できる方法が見つかり次第、本項目を修正します。

ダウンロードしたzip内にあるフォルダを、Cドライブ直下に置いてもらい、フォルダ名を「dictation-kit」に変更してください。

### Eel (※GUIアプリを使う場合)
以下のコマンドを入力し、実行してください。
```cmd:例
python -m pip install eel
```

## 実行
Google Chrome(ブックマークバー有)で雀魂を起動した後、以下のコマンドを入力してください。
- GUIアプリを起動する場合 python main-gui.py
- コンソールで起動する場合 python main.py

## さいごに
つらつらと書きましたが、まだこのメモで動作したか確認は取れてません。