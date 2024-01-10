Folder Synchroniser

This program synchronises a folder to an identical replica of itself, and prints logs to the terminal and to a log file. It works with files and sub-folders, 
but changes to files inside sub-folders are logged as changes to the sub-folder (the logs only concern activity at the root level of the source/replica folders).

This program passes 4 command-line arguments into main.py:
	1. Source folder path: this folder must exist for the program to run. You will be prompted if you provided a path that doesn’t exist.
	2. Replica folder path: if this doesn’t exist already, a new one will be created.
  3. Log file path: This will also be created if it doesn’t exist already
  4. Interval: This sets the interval in seconds for the synchronisation
