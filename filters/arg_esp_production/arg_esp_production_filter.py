'''
import json

from filters.twentieth_century.twentieth_century_filter import apply_filter
from middleware.consumer.consumer import Consumer
from middleware.producer.producer import Producer
from model.movie import movie_to_dict
from utils.parsers.movie_parser import convert_data

class ArgEspProductionFilter:

    def __init__(self, input_queue='cola_filtro_20'):
        self.movies_filtered = []
        self.consumer = Consumer(
            queue_name=input_queue,
            message_factory=self.handle_message
        )
        self.producer = Producer("cola_filtrada_20s")

    def handle_message(self, message_bytes: bytes):
        batch = json.loads(message_bytes.decode())
        movies = convert_data(batch)

        filtered_movies = apply_filter(movies)
        self.movies_filtered.extend(filtered_movies)

        if filtered_movies:
            encoded = json.dumps([movie_to_dict(m) for m in filtered_movies])
            self.producer.enqueue(encoded.encode())

        return movies'''