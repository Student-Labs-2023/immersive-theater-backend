FROM python:3.11.1-slim

WORKDIR /immersive-theater

COPY . /immersive-theater

RUN pip install --upgrade pip 

RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python", "app.py" ]
