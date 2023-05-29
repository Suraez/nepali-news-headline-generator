FROM python:3.8

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install tensorflow-intel

RUN pip install -r /app/requirements.txt

EXPOSE 5000

COPY . /app/

CMD [ "python", "server.py" ]