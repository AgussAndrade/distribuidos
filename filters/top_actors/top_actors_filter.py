import json
import logging
from middleware.consumer.consumer import Consumer
from middleware.producer.producer import Producer
from utils.parsers.movie_parser import convert_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TopActorsFilter:
    def __init__(self):
        #self.consumer_arg_esp_production = Consumer("arg_españa_production", message_factory=self.handle_message_arg_esp_production)  # Lee de la cola de movies
        self.consumer_actors = Consumer("actor", message_factory=self.handle_message_actors)  # Lee de la cola de movies
        #self.producer = Producer("arg_españa_production")  # Envía resultados a aggregate_consulta_1

    def handle_message_arg_esp_production(self, message):
        return message
        '''if message.get("type") == "shutdown":
            return message
        movies = convert_data(message)

        filtered_movies = apply_filter(movies)

        # Crear un mensaje con la información del batch
        batch_message = {
            "movies": [movie.to_dict() for movie in filtered_movies],
            "batch_size": message.get("batch_size", 0),
            "total_batches": message.get("total_batches", 0),
            "type": "batch_result"
        }

        return batch_message'''

    def handle_message_actors(self, message):
        return message

    def start(self):
        """Inicia el procesamiento de películas"""
        logger.info("Iniciando filtro de top 10 actores con mayo participacion")

        try:
            while True:
                message = self.consumer_actors.dequeue()
                if type(message) == dict and message.get("type") == "shutdown":
                    print("Shutting down filter")
                    break
                if not message:
                    continue
                #self.producer.enqueue(message)
        except KeyboardInterrupt:
            logger.info("Deteniendo filtro...")
        finally:
            self.close()

    def close(self):
        """Cierra las conexiones"""
        #self.consumer_arg_esp_production.close()
        self.consumer_actors.close()
        #self.producer.close()

def apply_filter(movies):
    pass
    # return [movie for movie in movies if movie.released_in_or_after_2000_argentina()]

if __name__ == '__main__':
    filter = TopActorsFilter()
    filter.start()