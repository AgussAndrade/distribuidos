import time
import json

from middleware.consumer.consumer import Consumer
from utils.parsers.movie_parser import convert_data


class ArgEspProductionFilter:
    def __init__(self, queue_name='cola'):
        self.movies_filtered = []
        self.consumer = Consumer(
            queue_name=queue_name,
            message_factory=self.handle_message
        )

    def handle_message(self, message_bytes: bytes):
        batch = json.loads(message_bytes.decode())
        movies = convert_data(batch)

        #filtered_movies = apply_filter(movies)
        #for movie in filtered_movies:
        #    self.movies_filtered.append(movie)

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
            # self.close()
if __name__ == '__main__':
    time.sleep(5)  # Espera para asegurarse que RabbitMQ está listo
    client = ArgEspProductionFilter()
    client.start()