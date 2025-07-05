import os

import redis
from iso639 import Lang

TVDB_API_KEY = os.getenv("TVDB_API_KEY")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
MUSICBRAINZ_API_KEY = os.getenv("MUSICBRAINZ_API_KEY")

METADATA_SERVER_FOR = os.getenv("METADATA_SERVER_FOR")

LANGS_FALLBACK = [Lang(lang) for lang in os.getenv("LANGS_FALLBACK", "eng").lower().split(",")]

INCLUDE_ADULT_CONTENT = os.getenv("INCLUDE_ADULT_CONTENT", "false").lower() in ("true", "1", "yes")

REDIS_CACHE = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=int(os.getenv("REDIS_DB", 0)),
    password=os.getenv("REDIS_PASSWORD", None),
    decode_responses=True,
)

METADATA_SERVER_FOR = METADATA_SERVER_FOR.lower().split(",") if METADATA_SERVER_FOR else None





class ArrServer:
    SONARR = "sonarr"
    RADARR = "radarr"
    LIDARR = "lidarr"
    READARR = "readarr"

    @staticmethod
    def get_all():
        return [ArrServer.SONARR, ArrServer.RADARR, ArrServer.LIDARR, ArrServer.READARR]

    @staticmethod
    def is_activated(s):
        return s in METADATA_SERVER_FOR

for server in METADATA_SERVER_FOR or []:
    if server not in ArrServer.get_all():
        raise ValueError(f"METADATA_SERVER_FOR values must be one of {', '.join(ArrServer.get_all())}. Got: {server}")

    # check if all required are matched (TVDB_API_KEY for sonarr, TMDB_API_KEY for radarr, MUSICBRAINZ_API_KEY for lidarr)
    match server:
        case ArrServer.SONARR:
            if not TVDB_API_KEY:
                raise ValueError("TVDB_API_KEY environment variable is not set for Sonarr")

        case ArrServer.RADARR:
            if not TMDB_API_KEY:
                raise ValueError("TMDB_API_KEY environment variable is not set for Radarr")

        case ArrServer.LIDARR:
            if not MUSICBRAINZ_API_KEY:
                raise ValueError("MUSICBRAINZ_API_KEY environment variable is not set for Lidarr")

        case _:
            # METADATA_SERVER_FOR value not supported at this time
            raise ValueError(server + " is not supported at this time. Supported values are 'sonarr', 'radarr', 'lidarr'")