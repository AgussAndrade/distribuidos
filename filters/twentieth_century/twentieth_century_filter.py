import time
import json

from middleware.consumer.consumer import Consumer
#from middleware.producer.producer import Producer
from model.movie import movie_to_dict
from utils.parsers.movie_parser import convert_data

class TwentiethCenturyFilter:
    #def __init__(self, queue_name='cola', next_queue='cola_filtro_20'):
    def __init__(self, queue_name='cola'):
        self.movies_filtered = []
        self.consumer = Consumer(
            queue_name=queue_name,
            message_factory=self.handle_message
        )
        #self.producer = Producer(next_queue)

    def handle_message(self, message_bytes: bytes):
        batch = json.loads(message_bytes.decode())
        movies = convert_data(batch)

        filtered_movies = apply_filter(movies)
        self.movies_filtered.extend(filtered_movies)

        if filtered_movies:
            encoded = json.dumps([movie_to_dict(m) for m in filtered_movies])
            #self.producer.enqueue(encoded.encode())

        return movies

    def start(self):
        try:
            print("[CONSUMER_CLIENT] Iniciando consumo de mensajes...")
            self.consumer.connect()

            while True:
                self.consumer.dequeue()
                time.sleep(1)

        except KeyboardInterrupt:
            print("[CONSUMER_CLIENT] Interrumpido por el usuario")
            #self.close()

    #def close(self):
        #self.consumer.close()

def apply_filter(movies):
    return [movie for movie in movies if movie.released_in_or_after_2000()]

