FROM python:3.10.12

WORKDIR /immersive-theater

COPY . /immersive-theater

RUN pip3.10 install -r requirements.txt

EXPOSE 5000

CMD [ "python3.10", "app.py" ]
