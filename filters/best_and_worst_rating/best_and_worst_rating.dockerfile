FROM python:3.9-slim
COPY middleware/consumer/consumer.py /root/middleware/consumer/consumer.py
COPY middleware/producer/producer.py /root/middleware/producer/producer.py
COPY filters/best_and_worst_rating/best_and_worst_rating.py /root/filters/best_and_worst_rating/best_and_worst_rating.py
COPY model/movie.py /root/model/movie.py
COPY utils/parsers/movie_parser.py /root/utils/parsers/movie_parser.py
RUN pip install pika
ENV PYTHONPATH="/root"
CMD ["python", "/root/filters/best_and_worst_rating/best_and_worst_rating.py"]