Caching reduces the number of queries carried out at execution by writing their results to disk for later reading.

## Cache directory

Cached dataframes are stored in `/df_cache` as `.feather` files. `.feather` files are used as the format instead
of `.csv` files to allow for the preservation of data types (e.g., date time).

The cache directory is included in [`.gitignore`](../.gitignore) so that cached files are not committed. The cache
directory is regenerated upon execution to ensure it always exists before any attempts to read cached files.

## Caching strategy

In SQL query functions, it is first checked whether the SQL query result as a dataframe is cached. This is done by
checking if the file exists in the cache directory. If the file exists, the dataframe is read from the file and
returned. If it does not, the SQL query is executed and saved to disk.

## Clearing the cache

The cache can be cleared by deleting the contents of the cache directory. This can be done manually or in command line.
In the repository directory, run the following comand to recursively remove all contents in the cache directory.

```zsh
rm -rf df_cache
```
