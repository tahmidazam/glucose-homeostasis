Data curation repository based on [`4yr_project_glucose`](https://github.com/GilesLuo/4yr_project_glucose)
by [Zhiyao Luo](https://github.com/GilesLuo).

> **Update**: This project was presented at the Institute of Biomedical Engineering, University of Oxford on Sep 2, 2024. You can find the presentation slides [here](https://www.figma.com/deck/20kLqTzfl5IgFfFQVMMEbr/Visitor-Day-Sep-2-2024).

## Prerequisites

To run this project locally, the following is required:

- Access to the [MIMIC-III Clinical Database](https://physionet.org/content/mimiciii/1.4/), which involves becoming a
  credentialed user and signing a data use agreement (find out more from
  the [MIMIC documentation](https://mimic.mit.edu/docs/gettingstarted/));
- Access to
  the [Curated Data for Describing Blood Glucose Management in the Intensive Care Unit](https://physionet.org/content/glucose-management-mimic/1.0.1/#files-panel),
  with similar involvements; and
- Access to [RxNav-in-a-Box](https://lhncbc.nlm.nih.gov/RxNav/applications/RxNav-in-a-Box.html) via a Unified Medical
  Language System (UMLS) license
  agreement.
- Access to the [Logical Observation Identifiers Names and Codes (LOINC) database](https://loinc.org/).

> **Note**: The RxNorm and RxClass APIs used inside RxNav-in-a-Box must be run locally. Read more
> at [Classifying prescriptions](/docs/prescriptions.md).

You can read documentation articles without running the project locally. Essential plots utilised in the literature are
pushed to enable this.

### System requirements

From the RxNav-in-a-Box [README.txt](https://data.lhncbc.nlm.nih.gov/public/rxnav/rxnav-in-a-box/README.txt):

> - "12 gigabytes of memory to devote to a container platform (e.g., Docker)
> - 100 gigabytes of disk space
> - Docker Desktop,
    or another OCI-compatible platform (in which case you
    may take the included docker-compose.yml file as an example)."

From
the [`mimic-code`](https://github.com/MIT-LCP/mimic-code/blob/main/mimic-iii/buildmimic/postgres/README.md#hard-drive-space-required)
repository:

> "Loading the data into a PostgreSQL database requires around ~47 GB of space. The addition of [optional] indexes adds
> another 26
> GB. You will likely want to reserve 100 GB for the entire database."

If running both the RxNav-in-a-Box and MIMIC-III databases locally, ensure that you have enough disk space and
memory:

- \>200GB disk space, and
- \>12GB memory.

[Docker Desktop](https://www.docker.com/products/docker-desktop/) is recommended for running RxNav-in-a-Box locally.

## Getting started

1. Clone this repository.
2. Download the `.zip` file containing the dataset _Curated Data for Describing Blood Glucose Management in the
   Intensive Care Unit_ (version 1.0.1)
   from [physionet.org](https://physionet.org/content/glucose-management-mimic/1.0.1/#files-panel), and uncompress it in
   the directory as the clone of this repository.
3. Download the `.zip` file containing the LOINC database from [loinc.org](https://loinc.org/downloads/) and uncompress
   it in the same directory as the clone of this repository.
4. Follow the instructions on [mimic.mit.edu](https://mimic.mit.edu/docs/gettingstarted/local/) to
   install [MIMIC-III](https://physionet.org/content/mimiciii/1.4/) to a local [PostgreSQL](https://www.postgresql.org)
   database. Update the `.env` file with your database credentials.
5. Set up your Python virtual environment.
6. Install required packages using `pip install -r requirements.txt`.
7. Set your environment variables in [`.env`](.env).
8. Run the `curation` module inside your virtual environment using `python -m curation`.

## Documentation

- [Curating demographics](docs/demographics.md)
- [Classifying prescriptions using RxNorm and RxClass](docs/prescriptions.md)
- [Classifying lab events using LOINC](docs/labevents.md)
- [Calculating weights and heights](docs/calculating-weights-and-heights.md)
- [Caching](docs/caching.md)

## Command-line arguments

| name or flags                  | type  | default   | description                                                                                                                                               |
|--------------------------------|-------|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `-l`, `--log-level`            | `str` | `warning` | The log level.                                                                                                                                            |
| `-m`, `--max-identifier-count` | `int` | `-1`      | The maximum number of unique ICU stays identifiers. Any number less than or equal to zero will not limit the number of identifiers, and all will be used. |
| `-c`, `--chunk_size`           | `int` | `1000`    | The chunk size to use when querying the database.                                                                                                         |

## Bibliography

- Johnson A, Pollard T, Mark R. MIMIC-III Clinical Database (version 1.4). PhysioNet. 2016. Available
  from: https://doi.org/10.13026/C2XW26.
- Robles Arévalo A, Mateo-Collado R, Celi L A. Curated Data for Describing Blood Glucose Management in the Intensive
  Care Unit (version 1.0.1). PhysioNet. 2021. Available from: https://doi.org/10.13026/517s-2q57.
- Nelson SJ, Zeng K, Kilbourne J, Powell T, Moore R. Normalized names for clinical drugs: RxNorm at 6 years. J Am Med
  Inform Assoc [Internet]. 2011 [cited 2024 Aug 1];18(4):441–8. Available
  from: https://academic.oup.com/jamia/article-lookup/doi/10.1136/amiajnl-2011-000116
- Vreeman DJ, McDonald CJ, Huff SM. LOINC® - A Universal Catalog of Individual Clinical Observations and Uniform
  Representation of Enumerated Collections. Int J Funct Inform Personal Med. 2010;3(4):273–91.

---

Tahmid Azam, [ta549@cam.ac.uk](mailto:ta549@cam.ac.uk)
