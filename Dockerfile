FROM python:slim

WORKDIR /immersive-theater

COPY . /immersive-theater

RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python", "app.py" ]
