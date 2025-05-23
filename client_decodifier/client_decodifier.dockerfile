FROM python:3.9-alpine

COPY client_decodifier/client_decodifier.py /root/client_decodifier/client_decodifier.py
COPY middleware/ /root/middleware/
COPY worker/worker.py /root/worker/worker.py

RUN pip install pika

ENV PYTHONPATH="/root"

CMD ["python", "/root/client_decodifier/client_decodifier.py"]