#画像の後処理　ラベルと信頼度を表示

import random
import cv2

def draw_texts(image, label):
    """認識した画像にラベルを追加"""
    cv2.rectangle(image, (0,0), (224,224), (0,255,0), 1)
    cv2.putText(image, label, (0,30), 0, 1, [255,255,255], thickness=2,
    lineType=cv2.LINE_AA)
