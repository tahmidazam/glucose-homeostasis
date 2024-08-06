from enum import Enum


class Filter(Enum):
    # Age
    AGE_LOWER_BOUND: int = 18
    AGE_UPPER_BOUND: int = 100

    # Length of stay
    LENGTH_OF_STAY_LOWER_BOUND: int = 1
    LENGTH_OF_STAY_UPPER_BOUND: int = 30

    # Height
    HEIGHT_UPPER_BOUND: int = 3

    # Weight
    WEIGHT_UPPER_BOUND: int = 300
