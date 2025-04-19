from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Movie:
    title: str
    production_countries: list[str]
    release_date: str
    type: str
    genres: List[str]
    budget: int

    def released_in_or_after_2000_argentina(self) -> bool:
        if not self.release_date or not self.production_countries:
            return False
        try:
            return int(self.release_date) >= 2000 and self.is_argentine()
        except Exception as e:
            print(f"[MOVIE] Error parseando fecha '{self.release_date}' en {self.title}: {e}")
            return False

    def to_dict(self):
        return {
            "title": self.title,
            "production_countries": self.production_countries,
            "release_date": self.release_date,
            "type": self.type,
            "genres": self.genres,
            "budget": self.budget
        }
    
    def get(self, attr: str):
        return getattr(self, attr)
    def is_argentine(self) -> bool:
        return 'AR' in self.production_countries