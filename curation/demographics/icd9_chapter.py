from enum import Enum


class ICD9Chapter(Enum):
    NEOPLASMS: tuple[int, ...] = tuple(range(140, 240))
    COMPLICATIONS_OF_PREGNANCY_CHILDBIRTH_AND_THE_PUERPERIUM: tuple[int, ...] = tuple(range(630, 680))
