from enum import Enum


class ICD9Chapter(Enum):
    NEOPLASMS: tuple[str, ...] = tuple([str(i) for i in range(140, 240)])
    COMPLICATIONS_OF_PREGNANCY_CHILDBIRTH_AND_THE_PUERPERIUM: tuple[str, ...] = tuple([str(i) for i in range(630, 680)])
