import os

import redis

TVDB_API_KEY = os.getenv("TVDB_API_KEY")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
MUSICBRAINZ_API_KEY = os.getenv("MUSICBRAINZ_API_KEY")

METADATA_SERVER_FOR = os.getenv("METADATA_SERVER_FOR")

TVDB_RESULT_LANG = os.getenv("TVDB_RESULT_LANG", "eng").lower()

REDIS_CACHE = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=int(os.getenv("REDIS_DB", 0)),
    password=os.getenv("REDIS_PASSWORD", None),
    decode_responses=True,
)

# enum with values "sonarr", "radarr", "lidarr", "readarr"
METADATA_SERVER_FOR = METADATA_SERVER_FOR.lower() if METADATA_SERVER_FOR else None
if METADATA_SERVER_FOR not in ["sonarr", "radarr", "lidarr", "readarr"]:
    raise ValueError("METADATA_SERVER_FOR must be one of 'sonarr', 'radarr', 'lidarr' or 'readarr'")

# check if all required are matched (TVDB_API_KEY for sonarr, TMDB_API_KEY for radarr, MUSICBRAINZ_API_KEY for lidarr)
match METADATA_SERVER_FOR:
    case "sonarr":
        if not TVDB_API_KEY:
            raise ValueError("TVDB_API_KEY environment variable is not set for Sonarr")

    case "radarr":
        if not TMDB_API_KEY:
            raise ValueError("TMDB_API_KEY environment variable is not set for Radarr")

    case "lidarr":
        if not MUSICBRAINZ_API_KEY:
            raise ValueError("MUSICBRAINZ_API_KEY environment variable is not set for Lidarr")

    case _:
        # METADATA_SERVER_FOR value not supported at this time
        raise ValueError(METADATA_SERVER_FOR + " is not supported at this time. Supported values are 'sonarr', 'radarr', 'lidarr'")