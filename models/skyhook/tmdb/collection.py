import json
from dataclasses import dataclass
from typing import List, Any

from tmdbsimple import Collections, Movies

from models.skyhook.tmdb.image import Image
from models.skyhook.tmdb.translation import Translation
from models.skyhook.tmdb.movie import Movie
from utils import TMDB_IMAGE_BASE_URL, set_attrs_from_dict


@dataclass
class Collection:
    TmdbId: int
    Name: str
    Overview: str
    Images: List[Image]
    Translations: List[Translation]
    Parts: List[Movie]

    @staticmethod
    def from_dict(obj: Any) -> 'Collection':
        _TmdbId = int(obj.get("TmdbId"))
        _Name = str(obj.get("Name"))
        _Overview = str(obj.get("Overview"))
        _Images = [Image.from_dict(y) for y in obj.get("Images")]
        _Translations = [Translation.from_dict(y) for y in obj.get("Translations")]
        _Parts = map(Movie.from_dict, obj.get("Parts", []))
        return Collection(_TmdbId, _Name, _Overview, _Images, _Translations, _Parts)

    @staticmethod
    def from_tmdb_obj(obj: Collections) -> 'Collection':

        images = []

        # add poster images
        if hasattr(obj, 'posters') and obj.posters:
            # get a poster with a filter
            posters = sorted(obj.posters, key=lambda x: x.get('vote_count', 0), reverse=True)

            images.append(Image(
                "Poster",
                TMDB_IMAGE_BASE_URL + posters[0].get("file_path"),
            ))

        if hasattr(obj, 'backdrops') and obj.backdrops:
            # get a backdrop with a filter
            backdrops = sorted(obj.backdrops, key=lambda x: x.get('vote_count', 0), reverse=True)

            images.append(Image(
                "Banner",
                TMDB_IMAGE_BASE_URL + backdrops[0].get("file_path"),
            ))

        return Collection(
            TmdbId=obj.id,
            Name=obj.name,
            Overview=obj.overview,
            Images=images,
            Translations=[Translation.from_tmdb_obj(translation) for translation in obj.translations],
            Parts=[]
        )