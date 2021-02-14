import socket
import time

HOST = '127.0.0.1'   # juliusサーバーのIPアドレス
PORT = 10500         # juliusサーバーの待ち受けポート
DATESIZE = 1024     # 受信データバイト数

class Julius:

    def __init__(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))
        self.fin_flag = False
        self.text = ""

    def Update(self):
        # juliusサーバからデータ受信
        data = self.sock.recv(DATESIZE).decode('utf-8')
        strTemp = ""
        for line in data.split('\n'):
            # 受信データから、<WORD>の後に書かれている言葉を抽出して変数に格納する。
            # <WORD>の後に、話した言葉が記載されている。
            index = line.find('WORD="')
            if index != -1:
                # strTempに話した言葉を格納
                strTemp = strTemp + line[index+6:line.find('"',index+6)]
                
            # 受信データに</RECOGOUT>'があれば、話終わり ⇒ フラグをTrue
            if '</RECOGOUT>' in line:
                self.fin_flag = True

        # 話した言葉毎に、print文を実行
        if self.fin_flag == True:
            self.text = strTemp.replace("[s]", "").replace("[/s]", "")
            self.fin_flag = False
            strTemp = ""

# t = Julius()

# while True:
#     t.Update()
#     print(t.text)