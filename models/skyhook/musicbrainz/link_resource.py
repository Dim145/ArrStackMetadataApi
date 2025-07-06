from dataclasses import dataclass
from typing import Optional


@dataclass
class LinkResource:
    Target: Optional[str] = None
    Type: Optional[str] = None

    @staticmethod
    def from_musicbrainz(obj: dict) -> 'LinkResource':
        """
        Create a LinkResource instance from a MusicBrainz link object.

        :param obj: A dictionary representing a link from MusicBrainz.
        :return: An instance of LinkResource.
        """
        return LinkResource(
            Target=obj.get('target'),
            Type=obj.get('type')
        )