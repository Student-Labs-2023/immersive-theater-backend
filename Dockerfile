FROM python:latest

WORKDIR /immersive-theater

COPY . /immersive-theater

RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python3", "app.py" ]
