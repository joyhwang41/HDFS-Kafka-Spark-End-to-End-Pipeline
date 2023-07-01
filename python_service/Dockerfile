FROM python:3.9

WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

# Copy source code
COPY . .

CMD ["python", "app.py"]
