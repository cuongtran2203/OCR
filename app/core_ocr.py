from paddleocr import PaddleOCR,draw_ocr
import numpy as np
import cv2
from PIL import Image
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
# to switch the language model in order.
ocr = PaddleOCR(lang='en',show_log=False) # need to run only once to download and load model into memory
Results={"pos":[],"text":[]}

def inference(img):
    image=np.array(img)
    image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    result = ocr.ocr(image, cls=False)
    result=result[0]
    # print(result)
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    # print(txts)
    results_txt=''
    txt=[]
    results_txt='\n'.join(t for t in txts)
    # print(results_txt)
    scores = [line[1][1] for line in result]
    im_show = draw_ocr(image, boxes, txts, scores, font_path='simfang.ttf')
    im_show = Image.fromarray(im_show)
    return results_txt,im_show
    