import pytesseract 
import numpy as np
import cv2
from time import sleep
from PIL import ImageGrab, Image
from matplotlib import pyplot as plt
import pyautogui as pag

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# tipando a leitura para os canais de ordem RGB
def capt():
    capture = ImageGrab.grab(bbox=(400,134,486,170))
    frame = np.array(capture)
    cor_n = cv2.cvtColor(frame,cv2.COLOR_BGR2RGBA)
    gray  = cv2.cvtColor(cor_n, cv2.COLOR_BGR2GRAY)
    muda_cor  = cv2.bitwise_not(gray)
    #edges = cv2.Canny(frame,500,500)
    lower= cv2.pyrUp(muda_cor)
    text = pytesseract.image_to_string(lower,lang='eng')
    score =  "".join(filter(str.isdigit,text))
    sleep(1)
    if (score == ""):
        score = "-1"
    else:
        return score


   

capt()