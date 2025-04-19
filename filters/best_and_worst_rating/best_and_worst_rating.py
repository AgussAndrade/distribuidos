import time
import json
from venv import logger

from middleware.consumer.consumer import Consumer
from middleware.producer.producer import Producer
from utils.parsers.movie_parser import convert_data


class ArgEspProductionFilter:
    def __init__(self):
        self.movies = None
        self.consumer_ratings = None # No consumimos de la cola de ratings hasta tener los resultados de
        self.consumer = Consumer(
            queue_name="result", # TODO cambiar nombre
            message_factory=self.handle_movies_result
        )
        self.producer = Producer("aggregate_consulta_4")

    def handle_movies_result(self, message):
        # Cuando nos llega el resultado de peliculas filtradas, podemos comenzar a consumir los ratings
        self.consumer_ratings = Consumer(
            queue_name="ratings",
            message_factory=self.handle_message
        )
        # TODO Cerrar el consumidor de movies
        self.movies = message.get("movies")

    def handle_message(self, message):
        if message.get("type") == "shutdown":
            return message

        best_and_worst = best_and_worst_ratings(message.get("movies"), message.get("ratings"))

        return batch_message


    def start(self):
        """Inicia el procesamiento de películas"""
        logger.info("Iniciando filtro de películas del siglo XXI")
        
        try:
            while True:
                message = self.consumer.dequeue()
                if type(message) == dict and message.get("type") == "shutdown":
                    print("Shutting down filter")
                    break
                if not message:
                    continue
                self.producer.enqueue(message)
        except KeyboardInterrupt:
            logger.info("Deteniendo filtro...")
        finally:
            self.close()

    def close(self):
        """Cierra las conexiones"""
        self.consumer.close()
        self.producer.close()

def best_and_worst_ratings(movies, ratings):
    # TODO aca se crea el resultado a partir de las peliculas filtradas y los ratings
    batch_message = {
        "best": filteredmovies_movies,
        "best_rating": message.get("batch_size", 0),
        "worst": message.get("total_batches", 0),
        "worst_rating": "batch_result"
    }
    return batch_message

if __name__ == '__main__':
    filter = ArgEspProductionFilter()
    filter.start()