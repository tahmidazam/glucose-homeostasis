## Weight-related items

Using the following SQL snippet, the item identifiers containing 'weight' in their label were queried.

```sql
SELECT itemid, label
FROM mimiciii.d_items
WHERE LOWER(label) LIKE '%%weight%%'
-- Query complete in 00:00:00.102
```

The query results were as follows:

| itemid | label                                                      |
|--------|------------------------------------------------------------|
| 580    | Previous Weight                                            |
| 581    | Previous WeightF                                           |
| 4183   | Birthweight (kg)                                           |
| 733    | Weight Change                                              |
| 763    | Daily Weight                                               |
| 3580   | Present Weight (kg)                                        |
| 3581   | Present Weight (lb)                                        |
| 3582   | Present Weight (oz)                                        |
| 3583   | Previous Weight (kg)                                       |
| 3692   | Weight Change (gms)                                        |
| 3693   | Weight Kg                                                  |
| 3723   | Birth Weight (kg)                                          |
| 7000   | ideal body weight                                          |
| 45271  | Chucks Pad Weight                                          |
| 226846 | Feeding Weight                                             |
| 224639 | Daily Weight                                               |
| 227854 | Weight Bearing Status                                      |
| 226512 | Admission Weight (Kg)                                      |
| 226531 | Admission Weight (lbs.)                                    |
| 225124 | Unintentional weight loss >10 lbs.                         |
| 226740 | APACHE II Diagnosistic weight factors - Medical            |
| 226741 | APACHE II Diagnosistic weight factors - Surgical emergency |
| 226742 | APACHE II Diagnosistic weight factors - Surgical           |

### Item selection

From this query, the following items were selected for relevance to patient weight:

| itemid | label                   |
|--------|-------------------------|
| 580    | Previous Weight         |
| 581    | Previous WeightF        |
| 763    | Daily Weight            |
| 224639 | Daily Weight            |
| 226512 | Admission Weight (Kg)   |
| 226531 | Admission Weight (lbs.) |
| 226846 | Feeding Weight          |

The item identifiers were hard coded into the weights querying logic.

```python
WEIGHT_ITEM_IDS = (580, 581, 763, 226846, 224639, 226512, 226531)
```

### Units of measure

The units of measure for all selected item identifers are kilograms, with the exception of `226531` which is in pounds.

```python
WEIGHT_CONVERSION_FACTORS = {
    580: 1,
    581: 1,
    763: 1,
    224639: 1,
    226512: 1,
    226531: 0.45359237,
    226846: 1
}
```

## Height-related items

Carrying out the same process for height-related items involved the following SQL snippet:

```sql
SELECT itemid, label
FROM mimiciii.d_items
WHERE LOWER(label) LIKE '%%height%%'
-- Query complete in 00:00:00.048
```

### Item selection

The query results were as follows:

| itemid | label         |
|--------|---------------|
| 216    | Height of Bed |
| 1394   | Height Inches |
| 226707 | Height        |
| 226730 | Height (cm)   |

#### Units of measure

To investigate the units of measure for each of these items, the following query was used, where `ITEM_ID` is the item
identifier.

```sql
SELECT DISTINCT valueuom
FROM mimiciii.chartevents
WHERE itemid IN (ITEM_ID)
-- Query complete in 00:00:00.042
```

#### Final selection

From these items, the following were selected as relevant to patient height, along with the conversion factor to metres:

| itemid | label         | Conversion factor to metres |
|--------|---------------|-----------------------------|
| 1394   | Height Inches | 0.0254                      |
| 226707 | Height        | 0.0254                      |
| 226730 | Height (cm)   | 0.01                        |

The item identifiers were hard coded into the heights querying logic.

```python
HEIGHT_ITEM_IDS = (1394, 226707, 226730)
HEIGHT_CONVERSION_FACTORS = {
    1394: 0.0254,
    226707: 0.0254,
    226730: 0.01
}
```