FROM python:3-alpine

COPY requirements.txt ./

COPY app/ ./app/

RUN pip install -r requirements.txt

EXPOSE 5000

CMD flask run --host 0.0.0.0