from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse,Response,FileResponse
from typing import List
from PIL import Image
import io
import numpy as np
from core_ocr import *
import uvicorn
# dynamic.py
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
import base64
import requests
import json
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
@app.post("/api/")
async def check_result(request: Request):
    data = await request.json()
    image_url = data.get("image_url", "")
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        # Đọc dữ liệu của ảnh từ response
        image_data = response.content
        # Chuyển đổi dữ liệu của ảnh thành định dạng PIL Image
        image = Image.open(io.BytesIO(image_data))
        result,img = inference(image)
    except:
        return {"Result":"Image error"}
    return {"Result":result}
if __name__=="__main__":
    
    uvicorn.run("main:app",host="0.0.0.0",port=1234,reload=True)