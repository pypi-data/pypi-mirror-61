from dataclasses import dataclass
import enum
from typing import List
from .episode import Episode


@enum.unique
class Classification(enum.Enum):
    """The global classification of a client"""
    N = 'Normal'
    M = 'Malignant'
    B = 'Benign'
    CI = 'Interval Case'


@enum.unique
class Site(enum.Enum):
    """Site/centre where the medical examination took place"""
    adde = 'adde'
    jarv = 'jarv'
    stge = 'stge'


@dataclass
class Client:
    """
    A client represents a patient who has attended the NHS screening programme.

    Each client will have one or more :class:`omidb.episode.Episode` s, for
    which (anonymised and pseudonymised) NBSS information can be found.

    :param id: Client identifier, typically a four letter ID followed by a
        series of digits, e.g. `optm1`, `demd7050`
    :param episodes: A list of :class:`omidb.episode.Episode` s associated with
        the client
    :param classification: Enumeration specifying the global classification of
        the client. Note that the classification is not extracted from NBSS,
        but is based on logic applied to to the within-event opinions.
    :param site: Enumeration signifying the clinical site/centre where
        screening took place
    """

    id: str
    episodes: List[Episode]
    classification: Classification
    site: Site
