from dataclasses import dataclass
from decimal import Decimal


@dataclass
class RatingResource:
    Count: int = 0
    Value: Decimal = Decimal('0')

    @staticmethod
    def from_musicbrainz(obj: dict) -> 'RatingResource':
        return RatingResource(
            Count=obj.get('votes-count', 0),
            Value=Decimal(obj.get('rating', '0')) if obj.get('rating') is not None else Decimal('0')
        )