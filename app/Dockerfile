FROM python:3.8

WORKDIR /app

ADD . /app
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
EXPOSE 8000
RUN pip install -r requirements.txt

CMD ["python","main.py"]
