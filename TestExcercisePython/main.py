import sub
import os
from sys import argv, exit


#   Fistly, validate command line arguments for count and character validity (for paths and time interval)
try:
    source_folder_path = argv[1].strip()
    replica_folder_path = argv[2].strip()
    log_file_path = argv[3].strip()
    interval = int(argv[4])
    if len(argv) > 5:
        print("\n\nERROR - - - Invalid argument count.\n\n")
        exit()  
    try:
        for path in (source_folder_path,replica_folder_path, log_file_path):
            os.mkdir(path + "_test")
            os.rmdir(path + "_test")
    except OSError:
        print("\n\nERROR - - - Invalid path.\n\n")
        exit()
except (IndexError):
    print("\n\nERROR - - - Invalid argument count.\n\n")
    exit()
except (ValueError):
    print("\n\nERROR - - - Invalid character(s).\n\n")
    exit()

#   Main program
sub.monitor_and_sync(
        source_folder_path = argv[1].lstrip().rstrip(),
        replica_folder_path = argv[2].lstrip().rstrip(),
        log_file_path = argv[3].lstrip().rstrip(),
        interval = int(argv[4]),
        source_hash_dict = {},
        replica_hash_dict = {}, 
        added_files = [], 
        removed_files = [], 
        updated_files = [], 
        log_list = [],
        countdown = False,
    )