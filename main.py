from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse,Response,FileResponse
from typing import List
from PIL import Image
import io
import numpy as np
from core_ocr import *
app = FastAPI()

# dynamic.py
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
import base64
 
app = FastAPI()
 
templates = Jinja2Templates(directory="templates")
 
@app.get("/")
def dynamic_file(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
 
@app.post("/predict/")
def predict(request: Request,file: UploadFile = File(...)):
    file_bytes = file.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    result,img = inference(image)
    img_ar=np.array(img)
    # img_ar=cv2.cvtColor(img_ar,cv2.COLOR_RGB2BGR)
    encode_frame = cv2.imencode('.jpg', img_ar)[1].tobytes()
    encoded_image = base64.b64encode(file_bytes).decode("utf-8")

    cv2.imwrite("res.jpeg",img_ar)
    with io.open("res.jpeg","rb") as f:
        data=f.read()
    encoded_image_1 = base64.b64encode(data).decode("utf-8")

    return templates.TemplateResponse(
        "index.html", {"request": request,  "img": encoded_image,"Res":result,"results_img":encoded_image_1})
