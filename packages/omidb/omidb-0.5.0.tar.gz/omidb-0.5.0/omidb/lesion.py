import itertools
from typing import List, Set, Dict, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum


transforms = {}
transforms['CystAspirated'] = lambda x: True if x == 'Y' else False

Side = Enum('Side', 'L R')

LesionCodeToLesionDescription = {
    'AS': 'Asymmetry',
    'CA': 'Calcification only',
    'CY': 'Cyst',
    'DS': 'Distortion',
    'LN': 'Lymph node',
    'MA': 'Mass',
    'MC': 'Mass with calcification',
    'NA': 'No significant abnormality',
    'ZZ': 'Clinical abnormality',
}

LesionDescriptionToLesionCode = {
    v: k for k, v in LesionCodeToLesionDescription.items()
}

LesionDescriptionCode = Enum(  # type: ignore
    'LesionDescriptionCode',
    list(LesionCodeToLesionDescription.keys())
)

LesionDescription = Enum(  # type: ignore
    'LesionDescription',
    list(LesionCodeToLesionDescription.values())
)


LesionPosition = Enum(  # type: ignore
    'LesionPosition',
    [
        ''.join(_) for _ in
        list(itertools.product('LR', 'ABCDE', '1234')) + ['LM', 'RM']
    ]
)


@dataclass
class Lesion:
    side: Side
    cyst_aspirated: Optional[bool] = None
    description: Optional[LesionDescriptionCode] = None
    position: Optional[LesionPosition] = None
    notes: Optional[str] = None
