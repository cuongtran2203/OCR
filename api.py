from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from pdf2image import convert_from_path
from paddleocr import PaddleOCR
from utils import *
import os
import cv2
from pdf2image import convert_from_path
app = FastAPI()
ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory

# Đường dẫn tới thư mục lưu trữ file uploaded
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Templates sử dụng Jinja2
templates = Jinja2Templates(directory="templates")

# Route cho trang chủ, hiển thị form upload
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route để xử lý việc upload file
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_name = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_name, "wb") as buffer:
        buffer.write(file.file.read())
    if ".pdf" in file_name:
        # OCR: Chuyển đổi PDF thành hình ảnh và nhận diện văn bản
        images = convert_from_path(file_name)
        Results=inference(ocr,images)
        cluster=postprocess(Results=Results)
    else:
        img=cv2.imread(file_name)
        Results=inference_image(ocr,img)
        cluster=postprocess_image(Results)
        
    return {"filename": file.filename,"results":cluster}


    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
