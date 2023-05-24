FROM python:latest

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

EXPOSE 5000

COPY . /app/

CMD [ "python", "server.py" ]