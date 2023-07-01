FROM python:3.9

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

ENV PYTHONNONBUFFER 1

CMD ["python", "./app.py"]
  
