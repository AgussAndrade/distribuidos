import time
import json
from venv import logger

from middleware.consumer.consumer import Consumer
from middleware.producer.producer import Producer
from utils.parsers.movie_parser import convert_data


class BestAndWorstRating:
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
        return None

    def handle_message(self, message):
        if message.get("type") == "shutdown":
            return message

        best_and_worst = self.best_and_worst_ratings(self.movies, message.get("ratings"))

        return best_and_worst

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
    movie_ratings = {}
    for rating in ratings:
        movie_id = rating.get("movie_id")
        movie_rating = rating.get("rating")
        if movie_id and movie_rating is not None:
            if movie_id not in movie_ratings:
                movie_ratings[movie_id] = {"sum": 0, "count": 0}
            movie_ratings[movie_id]["sum"] += movie_rating
            movie_ratings[movie_id]["count"] += 1

    if not movie_ratings:
        return {
            "best": None,
            "best_rating": None,
            "worst": None,
            "worst_rating": None
        }

    average_ratings = {}
    for movie_id, data in movie_ratings.items():
        average_ratings[movie_id] = data["sum"] / data["count"]

    best_rated_movie = None
    worst_rated_movie = None
    best_rating = -1
    worst_rating = float('inf')

    movie_index = {movie.get("id"): movie for movie in movies if movie.get("id") is not None}

    for movie_id, avg_rating in average_ratings.items():
        movie = movie_index.get(movie_id)
        if movie:
            if avg_rating > best_rating:
                best_rating = avg_rating
                best_rated_movie = movie
            if avg_rating < worst_rating:
                worst_rating = avg_rating
                worst_rated_movie = movie

    batch_message = {
        "best": best_rated_movie.get("title") if best_rated_movie else None,
        "best_rating": best_rating if best_rated_movie else None,
        "worst": worst_rated_movie.get("title") if worst_rated_movie else None,
        "worst_rating": worst_rating if worst_rated_movie else None
    }

    return batch_message

if __name__ == '__main__':
    filter = BestAndWorstRating()
    filter.start()