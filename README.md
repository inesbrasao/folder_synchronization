# Directory sync script

This script provides a simple command-line utility to synchronize the contents
between two directories. It has been designed to sync at a user-specified
interval and will ensure that the target directory, "replica", is kept in sync
with the specified "source" directory.

## Features

- **One-way Synchronization**: Ensures that the contents of the replica are
  synced from the source directory. Works with nested directories.
- **MD5 Hash Comparison**: Uses md5 hash to detect changes in files, ensuring
  that only modified files are copied.
- **Logging**: Tracks the synchronization process into a log file, including
  file creation, updates, and deletions.


## Usage

To run the script, use the following command:

```
python3 sync.py --source_path <source_dir> --replica_path <replica_dir> --log_path <log_file> --interval <sync_interval>
```

Where interval is given in seconds.

## Tests

To run the tests, use the following command:
```
pytest
```




