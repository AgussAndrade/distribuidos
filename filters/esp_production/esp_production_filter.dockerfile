FROM python:3.9-alpine
COPY middleware/consumer/consumer.py /root/middleware/consumer/consumer.py
COPY middleware/producer/producer.py /root/middleware/producer/producer.py
COPY filters/esp_production/esp_production_filter.py /root/filters/esp_production/esp_production_filter.py
COPY model/movie.py /root/model/movie.py
COPY worker/worker.py /root/worker/worker.py
COPY utils/parsers/movie_parser.py /root/utils/parsers/movie_parser.py
RUN pip install pika
ENV PYTHONPATH="/root"
CMD ["python", "/root/filters/esp_production/esp_production_filter.py"]