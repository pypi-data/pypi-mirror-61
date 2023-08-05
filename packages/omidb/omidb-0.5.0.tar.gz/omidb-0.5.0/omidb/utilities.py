import enum
import datetime
from typing import Iterable, Optional


def str_to_date(date: str) -> datetime.date:
    if '-' in date:
        return datetime.datetime.strptime(date, '%Y-%m-%d').date()
    else:
        return datetime.datetime.strptime(date, '%Y%m%d').date()


def enum_lookup(value: str, e: Iterable[enum.Enum]) -> Optional[enum.Enum]:
    for member in list(e):
        if (value == member.name or value == member.value):
            return member
    return None
