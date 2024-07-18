## Prerequisites

1. Clone this repository.
2. Download the `.zip` file containing the dataset _Curated Data for Describing Blood Glucose Management in the
   Intensive Care Unit_ (version 1.0.1)
   from [physionet.org](https://physionet.org/content/glucose-management-mimic/1.0.1/#files-panel), and uncompress it in
   the directory as the clone of this repository.
3. Follow the instructions on [mimic.mit.edu](https://mimic.mit.edu/docs/gettingstarted/local/) to
   install [MIMIC-III](https://physionet.org/content/mimiciii/1.4/) to a local [PostgreSQL](https://www.postgresql.org)
   database.
4. Set up your Python virtual environment and install required packages using `pip install -r requirements.txt`.

## Caching dataframes

The dataframes from large SQL queries are cached in the `df-cache/` directory. To clear the cache, run `rm -rf df-cache`
which forcibly and recursively deletes the contents of the cache directory. The directory is regenerated if it does not
exist.

## Bibliography

- Johnson A, Pollard T, Mark R. MIMIC-III Clinical Database (version 1.4). PhysioNet. 2016. Available
  from: https://doi.org/10.13026/C2XW26.
- Robles Arévalo A, Mateo-Collado R, Celi L A. Curated Data for Describing Blood Glucose Management in the Intensive
  Care Unit (version 1.0.1). PhysioNet. 2021. Available from: https://doi.org/10.13026/517s-2q57.