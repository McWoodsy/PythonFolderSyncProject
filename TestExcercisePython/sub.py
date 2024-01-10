import sync_service
from datetime import datetime, timedelta
import time

def monitor_and_sync(
    source_folder_path,
    replica_folder_path,
    log_file_path,
    interval,
    source_hash_dict,
    replica_hash_dict, 
    added_files, 
    removed_files, 
    updated_files, 
    log_list,
    countdown,
    
    ):
    
    while True:
        #   Here the time interval is established
        start_time = datetime.now()
        cutoff = start_time + timedelta(seconds=interval)

        while countdown == False:
            
            #   Populate dicts of either folder to compare hashes
            #   if there are issues with the provided source path, we use recursion
            #   to reassign its value. It is then returned all the way back up to 
            #   this point to avoid issues with synchronization
            source_folder_path = sync_service.populate_dicts_final(
                source_folder_path,
                source_hash_dict,
                replica_folder_path,
                replica_hash_dict, 
                added_files, 
                removed_files, 
                updated_files, 
                log_file_path,
                log_list
                )
                
            #   Create lists of file names to determine which copy/remove operations are needed for which files
            sync_service.populate_to_do_lists(
                replica_folder_path,
                source_folder_path,
                removed_files,
                added_files,
                updated_files, 
                replica_hash_dict,
                source_hash_dict,
                log_file_path, 
                log_list
                )
            
            #   Check countdown timer
            if datetime.now() > cutoff:
                countdown = True
                
            sync_service.clear_dicts(source_hash_dict, replica_hash_dict)
            
        # Perform copy/remove operations based on contents of file lists when countdown is finished
        sync_service.synchronize(
            added_files, 
            removed_files, 
            updated_files, 
            source_folder_path, 
            replica_folder_path
            )
        
        sync_service.clear_todo_lists(
            added_files, 
            removed_files, 
            updated_files,
            log_list
            )
        
        time.sleep(1)
        countdown = False