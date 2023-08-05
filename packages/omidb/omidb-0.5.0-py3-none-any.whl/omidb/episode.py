import datetime
from dataclasses import dataclass
from typing import Optional, List
import enum
from .events import Events
from .study import Study
from .lesion import Lesion


@enum.unique
class Type(enum.Enum):
    """Type of episode"""
    CA = 'Continued Assessment'
    CD = 'Delayed Treatment'
    CF = 'Follow-up after treatment'
    CI = 'Interval case'
    CR = 'Local Recurrence'
    F = 'First Call'
    G = 'GP Referral'
    H = 'Higher Risk'
    N = 'Non-rout Recall'
    R = 'Routine Recall'
    S = 'Self Referral'
    X = 'Other'


@enum.unique
class Action(enum.Enum):
    """Episode action"""
    EC = 'Early Recall for Clinic'
    ES = 'Early Recall for Screening'
    FN = 'Fine Needle Aspiration'
    FP = 'Follow-up (Post-treatment)'
    FV = 'Further X-ray views'
    IP = 'Inpatient biopsy'
    MT = 'Medical Treatment'
    NA = 'No Action from this procedure'
    R2 = 'Routine second film opinion (obsolete)'
    RC = 'Review in clinic'
    RF = 'Referral to consultant/GP'
    RR = 'Routine recall for screening'
    ST = 'Surgical Treatment'
    TR = 'Repeat Film (technical)'
    WB = 'Wide Bore Needle'


@dataclass
class Episode:
    """
    An episode contains a set of medical procedures or events associated with
    the treatment or diagnosis of a clinical condition. Medical imaging studies
    are included with each episode, and are typically (but not always) linked
    to one or more events.

    :param id: NBSS episode identifier, only unique within client
    :param events: A set of medical procedures associated with the episode
    :param studies: List of :class:`omidb.study.Study` s where collections of
        screening and diagnostic images reside
    :param type: Enumeration defining the type of episode
    :param action: Enumeration defining the action outcome of the episode
    :param opened_date: Date that the episode opened
    :param closed_date: Date that the episode closed
    :param is_closed: boolean signifying whether the episode is closed
    :param lesions: A list of :class:`omidb.lesion.Lesion` s, examined in the
        episode
    """
    id: str
    events: Events
    studies: List[Study]
    type: Optional[Type] = None
    action: Optional[Action] = None
    opened_date: Optional[datetime.date] = None
    closed_date: Optional[datetime.date] = None
    is_closed: Optional[bool] = None
    lesions: Optional[List[Lesion]] = None
