FROM python:3.9-slim
COPY middleware/consumer/consumer.py /root/middleware/consumer/consumer.py
COPY filters/arg_esp_production/arg_esp_production_filter.py /root/filters/arg_esp_production/arg_esp_production_filter.py
COPY model/movie.py /root/model/movie.py
COPY utils/parsers/movie_parser.py /root/utils/parsers/movie_parser.py
RUN pip install pika
ENV PYTHONPATH="/root"
CMD ["python", "/root/filters/arg_esp_production/arg_esp_production_filter.py"]