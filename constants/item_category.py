from enum import Enum


class ItemCategory(Enum):
    HEIGHT_ITEM_IDS: [int, ...] = (1394, 226707, 226730)
    HEIGHT_CONVERSION_FACTORS = {
        1394: 0.0254,
        226707: 0.0254,
        226730: 0.01
    }

    WEIGHT_ITEM_IDS: tuple[int, ...] = (580, 581, 763, 226846, 224639, 226512, 226531)
    WEIGHT_CONVERSION_FACTORS = {
        580: 1,
        581: 1,
        763: 1,
        224639: 1,
        226512: 1,
        226531: 0.45359237,
        226846: 1
    }
