from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Movie:
    title: str
    production_countries: list[str]
    release_date: str
    genres: list[str]

    def released_in_or_after_2000(self) -> bool:
        if not self.release_date:
            return False
        try:
            return int(self.release_date) > 2000
        except Exception as e:
            print(f"[MOVIE] Error parseando fecha '{self.release_date}' en {self.title}: {e}")
            return False

def movie_to_dict(movie: Movie) -> dict:
    return asdict(movie)

def dict_to_movie(data: dict) -> Movie:
    return Movie(
        title=data.get("title", ""),
        production_countries=data.get("production_countries", []),
        release_date=data.get("release_date", ""),
        genres=data.get("genres", [])
    )