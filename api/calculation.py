from pathlib import Path
import json

import numpy as np
import cv2
import torch
from torchvision import models, transforms
from flask import current_app, jsonify


from study_api.api.postprocess import draw_texts
from study_api.api.preparation import load_image
from study_api.api.preprocess import image_to_tensor

basedir = Path(__file__).parent.parent

#出力結果からラベルを予測するクラス
class ILSVRC():
    """"ILSVRCデータに対するモデルの出力からラベルを求める"""
    def __init__(self, class_index):
        self.class_index = class_index

    def predict_max(self, out):
        """確率最大のラベル名の取得"""
        maxid = np.argmax(out.detach().numpy())
        predicted_label_name = self.class_index[str(maxid)][1]

        return predicted_label_name


#実際に入力画像から予測を行う
def recognition(request):
    #ラベルをjson形式から展開する
    LABEL = json.load(open('./data/imagenet_class_index.json', 'r'))
    predictor = ILSVRC(LABEL)

    #画像読み込み
    image, filename = load_image(request)
    #画像の前処理を行う
    img_transformed = image_to_tensor(image)
    inputs = img_transformed.unsqueeze_(0)
    #result_imageとしてnumpy配列型にする　draw_textsに代入する用
    result_image = np.array(image.copy())


    #学習済みモデルの読み込み
    try:
        model = torch.load("model.pt")
    except FileNotFoundError:
        return jsonify("The model is not found"), 404
    
    #モデルを推論モードに切り替え、推論の実行
    model = model.eval()
    output = model(inputs)
    result = predictor.predict_max(output)
    #画像に予測されるラベルを追加
    draw_texts(result_image, result)

    #画像保存先のパスを作成
    dir_image = str(basedir/"data"/"output"/filename)
    #画像認識後の画像を保存先に保存
    cv2.imwrite(dir_image, 
    cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR))
    return jsonify(result)