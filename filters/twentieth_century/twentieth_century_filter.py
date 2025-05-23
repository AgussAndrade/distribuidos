import logging

from middleware.consumer.consumer import Consumer
from middleware.producer.producer import Producer
from utils.parsers.movie_parser import convert_data
from worker.worker import Worker


logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%H:%M:%S')


class TwentiethCenturyFilter(Worker):
    def __init__(self):
        super().__init__()
        self.consumer = Consumer("movie", _message_handler=self.handle_message)
        self.producer = Producer("twentieth_century")

    def close(self):
        logger.info("Cerrando conexiones del worker...")
        try:
            self.consumer.close()
            self.producer.close()
            self.shutdown_consumer.close()
        except Exception as e:
            logger.error(f"Error al cerrar conexiones: {e}")

    def start(self):
        logger.info("Iniciando filtro de películas del siglo XXI")
        self.consumer.start_consuming()

    def handle_message(self, message):

        movies = convert_data(message)
        logger.info(f"Mensaje de peliculas sin filtrar recibido: {len(movies)} peliculas")
        filtered_movies = self.apply_filter(movies)
        logger.info(f"Se encontraron {len(filtered_movies)} peliculas de la decada de los 2000")

        total_batches = message.get("total_batches", 0)
        client_id = message.get("client_id")

        if total_batches != 0:
            logger.info(f"Este es el mensaje con total_batches: {total_batches} del cliente {client_id}")

        result = {
            "movies": [movie.to_dict() for movie in filtered_movies],
            "batch_size": message.get("batch_size", 0),
            "total_batches": total_batches,
            "type": "batch_result",
            "client_id": client_id
        }

        self.producer.enqueue(result)

    @staticmethod
    def apply_filter(movies):
        return [movie for movie in movies if movie.released_in_or_after_2000()]


if __name__ == '__main__':
    worker = TwentiethCenturyFilter()
    worker.start()
