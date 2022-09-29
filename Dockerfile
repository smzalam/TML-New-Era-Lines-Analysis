FROM python:3.10.6

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD uvicorn api.main:app --host 127.0.0.1 --reload --port 8000
