from enum import Enum


class FilterInfo(Enum):
    AGE_LOWER_BOUND: int = 18
    AGE_UPPER_BOUND: int = 100

    LENGTH_OF_STAY_LOWER_BOUND: int = 1
    LENGTH_OF_STAY_UPPER_BOUND: int = 30

    HEIGHT_UPPER_BOUND: int = 3
    WEIGHT_UPPER_BOUND: int = 300
