from ctypes.wintypes import HACCEL
from posixpath import dirname
from typing import Text
import cv2
from PyQt6 import uic,  QtCore, QtGui, QtWidgets
import sys, os
from PyQt6.QtWidgets import *
import pyautogui as pag
import res_rc
from PIL import ImageGrab
import numpy as np
from mss import mss
from PyQt6.QtGui import QImage
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTime, QTimer
import ocr
from time import sleep
import pytesseract
from matplotlib import pyplot as plt

width = 50
height = 50
xa = 0
ya = 0


#=============================#

tamanho = []
lista = []
fotos = ''
base = ''
count = 0
dados = 'n'
#===========================#
#(449, 139, 461, 377)
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# tipando a leitura para os canais de ordem RGB
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Ui_page(QWidget):

    def __init__(self):
        super().__init__()
        uic.loadUi("tela.ui", self)
        self.setWindowTitle("Project")
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.pushButton.setToolTip('text')
        self.pushButton.clicked.connect(self.hello)
        self.pushButton_7.clicked.connect(self.view)
        self.pushButton_8.clicked.connect(self.closex)
        self.pushButton_2.clicked.connect(self.get_valor)
        self.pushButton_9.clicked.connect(self.mouse_pos)
        self.pushButton_10.clicked.connect(self.start)
        self.pushButton_11.clicked.connect(self.pause)
        self.pushButton_12.clicked.connect(self.re_set)
        self.scree_tela = QtGui.QShortcut(QtGui.QKeySequence('r'), self)
        self.scree_tela.activated.connect(self.screen_position)
       
        #================CASCADE ==============================#
       
        self.face_cascade = cv2.CascadeClassifier('classifier/cascade.xml')
        self.count = 0
        # creating flag
        self.flag = False
        # creating a timer object
        timer = QTimer(self)
        # adding action to timer
        timer.timeout.connect(self.showTime)
        # update the timer every tenth second
        timer.start(100)
    # ===============================================================================#
           
    def showTime(self):
        if self.flag:
           self.count +=1
        self.text = str(self.count / 10)
        self.stopwatch_label.setText(self.text)
        if self.text == "13.0":
            pag.press("v")
        elif self.text == "16.0":
            if ocr.capt()!= None:
                a = ocr.capt()
                pag.click('acpt2.png')
                pag.doubleClick()
                sleep(1)
                resul = str(a)
                pag.write(resul)
                sleep(1)
                pag.click('acpt3.png')
                sleep(1)
                pag.doubleClick()
                self.count = 0
            else:
                self.count = 0

        
    def start(self):
        self.flag = True

    def pause(self):
        self.flag = False

    def re_set(self):
        self.flag = False       
        self.count = 0
        self.stopwatch_label.setText(str(self.count))
        

    def hello(self):
        global fotos
        fotos = self.input.text()
        dirName = f'{fotos}'
        f = os.path.abspath(dirName)
        global base
        base, file = os.path.split(f)
        if not os.path.exists(dirName):
            os.mkdir(dirName)
            self.input_aviso.setText("Pasta criada!!!")
        else:
            self.input_aviso.setText("Pasta ja existe")
   
    def foto(self):
        global count
        x, y = pag.position()
        count = count + 1
        nomeArquivo = ('/img ' + str(count) + '.png')
        foto = pag.screenshot(region=(x, y, 50, 50))
        foto.save("peixe-vemelho" + nomeArquivo)


#=================== Tela Mover =================================#

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
        self.dragPos = event.globalPosition().toPoint()
        event.accept()
#===============================================================#

    def mouse_pos(self):
        xa =0 
        ya =0
        while(True):
            with mss() as sct:
                global count
                x, y = pag.position()
                area = {
                "top": int(y - height / 2),
                "left": int(x - width / 2),
                "width": int(width),
                "height": int(height)
                }
            im = np.array(sct.grab(area))
            cv2.imshow('preview', im)
            k = cv2.waitKey(1)
            if k == ord('q'):
                break
            if k == ord('s'):
                cv2.imwrite(dados+'/objeto_{}.jpg'.format(count),im)
                count = count + 1 
    cv2.destroyAllWindows()

#=============================================================================#

    def screen_position(self):
        x, y = pag.position()
        text = f'x: {x},  y: {y}'
        self.input_posi.setText(text)

    def get_valor(self):
        try:
            valor_x = self.posi_x.text()
            valor_y = self.posi_y.text()
            valor_w = self.posi_a.text()
            valor_h = self.posi_b.text()
            img = ImageGrab.grab(bbox=(int(valor_x),int(
                valor_y), int(valor_w), int(valor_h)))

            #img = pag.screenshot(region=(int(valor_x), int(
                #valor_y), int(valor_w), int(valor_h)))
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame', frame)
        except:
            self.label_9.setText("Campo vazio Preencha o campo")




    def move_click(self, x , y ):
        pag.moveTo(x , y)
        pag.rightClick()
        
        #time.sleep(3)
        #pag.press('c')
        #time.sleep(3)
   

    def view (self):
        print('Starting...')
        sleep(1)
        print('Starting... 1')
        sleep(1)
        print('Starting... 2')
        sleep(1)
        print('Starting... 3')
        sleep(1)
        
        while True:
            img = ImageGrab.grab(bbox=(9,198,740,398))
            frame = np.array(img)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray,scaleFactor=6,minNeighbors=50)
            for(x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)
                area ={
                    "x":int(x+w/2),
                    "y":int(y+198+(h/2)),
                    "heigth":int(h)
                }
                area["y"] + 2
                self.area = area
                self.move_click(self.area["x"], self.area["y"])
                
                

            
            cv2.imshow("frame",frame)
            
            if cv2.waitKey(1) == ord('q'):
                break
        cv2.destroyAllWindows()

    def hacker(self):
        pass
   
        

    def closex(self):
        window.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_page()
    window.show()
    sys.exit(app.exec())
