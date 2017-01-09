* stage.py  

This script stages a number of files from tape. The paths should be listed in a file called "files" with the following format:
`/pnfs/grid.sara.nl/data/...`

You can change the pin lifetime in "srmv2_desiredpintime" attribute in seconds. In this example files stay pinned for a week.

* state.py

This script will display the status of each file listed in "files". The paths should be listed in a file called "files" with the following format:
`/pnfs/grid.sara.nl/data/...`.

Script output:

> ONLINE: means that the file is only on disk
> NEARLINE: means that the file in only on tape
> ONLINE_AND_NEARLINE: means that the file in on disk and tape

* Executing stage.py or state.py
  * Test the status of the files: `python state.py`
  * Bring the data online: `python stage.py`

