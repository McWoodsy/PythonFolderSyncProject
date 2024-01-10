import hashlib
import os
from datetime import datetime
import shutil

#   For extracting the basename from a filepath
def get_file_name(file_path):
    return os.path.basename(file_path)

#   Returns a file object for a specified file
def get_file(file_name, file_directory):
    file_path = os.path.join(file_directory, file_name)
    if os.path.isfile(file_path):
        return open(file_path, 'rb')
    else:
        return None

#   Calls folder hashing function if performed on a folder
def get_file_hash(file_path,log_list):
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            md5_hash = hashlib.md5()
            md5_hash.update(file.read()) 
        hashed_data = md5_hash.hexdigest()
    else:
        hashed_data = get_folder_hash(file_path,log_list)
    return hashed_data

#   If the file in the file list is not a file but a folder, we call this function again
def get_folder_hash(folder_path,log_list):
    md5_hash = hashlib.md5()
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            file_hash = get_file_hash(file_path, log_list)
            md5_hash.update(file_hash.encode('utf-8'))
            log_list.append(file)
        else:
            folder_hash = get_folder_hash(file_path, log_list)
            log_list.append(file)
            md5_hash.update(folder_hash.encode('utf-8'))
    hashed_data = md5_hash.hexdigest()
    return hashed_data

#   Writes to the terminal as well as the log
def write_to_log(file_name, log_file_path, action):
    try:  
        with open(log_file_path, 'a') as log_file:
            if action == "update":
                log_file.write("\n" + file_name + " was updated on " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
                print("\n" + file_name + " was updated on " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")+ "\n")
            elif action == "remove":
                log_file.write("\n" + file_name + " was removed on " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")+ "\n")
                print("\n" + file_name + " was removed on " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")+ "\n")
            elif action == "add":
                log_file.write("\n" + file_name + " was added on " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")+ "\n")
                print("\n" + file_name + " was added on " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")+ "\n")
    except FileNotFoundError:
        print("\n\nLog file not found. Creating new log now...")
        os.mkdir(log_file_path)
        write_to_log(file_name, log_file_path, action)

#   This copies a file from source to replica:
def copy(source_folder_path, replica_folder_path, file_name):
    shutil.copy(os.path.join(source_folder_path, file_name), os.path.join(replica_folder_path, file_name))

#   Cleans up the dictionaries to avoid errors
def clear_dicts(replica_hash_dict,source_hash_dict ):
    replica_hash_dict.clear()
    source_hash_dict.clear()
    
#   Clears lists to avoid errors
def clear_todo_lists(added_files, removed_files, updated_files,log_list):
    added_files.clear()
    removed_files.clear()
    updated_files.clear()
    log_list.clear()
    
#   Performing the actual sync based on which file is in which list
def synchronize(added_files, removed_files, updated_files, 
                source_folder_path, replica_folder_path):
    
    for file in added_files:
        try:
            if os.path.isfile(os.path.join(source_folder_path, file)):
                copy(source_folder_path, replica_folder_path, file)
            else:
                shutil.copytree(os.path.join(source_folder_path, file), os.path.join(replica_folder_path,file))
        except FileNotFoundError:
            print()
            
    for file in removed_files:
        try:
            if os.path.isfile(os.path.join(replica_folder_path, file)):
                os.remove(os.path.join(replica_folder_path, file))
            else:
                shutil.rmtree(os.path.join(replica_folder_path, file))
        except FileNotFoundError:
            print()

    for file in updated_files:
        try:
            if os.path.isfile(os.path.join(source_folder_path, file)):
                copy(source_folder_path, replica_folder_path, file)
            else:
                shutil.rmtree(os.path.join(replica_folder_path, file))
                shutil.copytree(os.path.join(source_folder_path, file), os.path.join(replica_folder_path, file))
        except FileNotFoundError:
            print()

#   Creates dictionary of filename and it's hash for accurate comparisons of files
def populate_source_dict(source_folder_path,source_hash_dict, log_list,
                              replica_folder_path,replica_hash_dict, added_files, 
                              removed_files, updated_files):
    try:    
        for file_name in os.listdir(source_folder_path):
            if file_name == '.DS_Store':
                continue
            file_path = os.path.join(source_folder_path, file_name)
            if os.path.isfile(file_path):
                file_name = get_file_name(file_path)
                file_hash = get_file_hash(file_path,log_list)
                source_hash_dict[file_name] = file_hash
            else: 
                folder_hash = get_folder_hash(file_path,log_list)
                source_hash_dict[file_name] = folder_hash
        return source_folder_path
                
    except FileNotFoundError:
        print("\n\nSource folder not found.\n\n")
        print("\n\nPlease re-enter source folder path")
        corrected_source_path = input()
        corrected_source_path = populate_source_dict(corrected_source_path,source_hash_dict, log_list,
                                                     replica_folder_path,replica_hash_dict, added_files, 
                                                     removed_files, updated_files
                                                     )
        return corrected_source_path  
        
#   Creates dictionary of filename and it's hash for accurate comparisons of files 
def populate_replica_dict(replica_folder_path,replica_hash_dict,  source_hash_dict, 
                          log_list, added_files, removed_files, updated_files):
    try:
        for file_name in os.listdir(replica_folder_path):
            if file_name == '.DS_Store':
                continue
            file_path = os.path.join(replica_folder_path, file_name)
            if os.path.isfile(file_path):
                file_name = get_file_name(file_path)
                file_hash = get_file_hash(file_path,log_list)
                replica_hash_dict[file_name] = file_hash
            else: 
                folder_hash = get_folder_hash(file_path, log_list)
                replica_hash_dict[file_name] = folder_hash
    except FileNotFoundError:
            print("\n\nReplica folder does not exist. Creating now...")
            os.mkdir(replica_folder_path)
            populate_replica_dict(replica_folder_path,replica_hash_dict,  
                                  source_hash_dict, log_list, added_files, 
                                  removed_files, updated_files
                                  )

def populate_dicts_final(source_folder_path,source_hash_dict,replica_folder_path,
                         replica_hash_dict, added_files, removed_files, 
                         updated_files, log_file_path, log_list):
    
    source_folder_path = populate_source_dict(source_folder_path,source_hash_dict, log_list,replica_folder_path,replica_hash_dict, added_files, removed_files, updated_files)
    populate_replica_dict(replica_folder_path,replica_hash_dict, source_hash_dict, log_list, added_files, removed_files, updated_files)
    return source_folder_path
     
#   Based on file names and file hashes, here we determine which files to put in which list for final sync step
def populate_to_do_lists(replica_folder_path,source_folder_path,
                         removed_files,added_files,updated_files, 
                         replica_hash_dict,source_hash_dict,
                         log_file_path,log_list):
    populate_removed_files_list(replica_folder_path, source_folder_path, 
                                removed_files,log_file_path,log_list)
    populate_added_files_list(source_folder_path,added_files,
                              replica_folder_path,log_file_path,log_list)
    populate_updated_files_list(replica_hash_dict,source_hash_dict,log_file_path,
                                updated_files,source_folder_path,log_list)   
     
def populate_updated_files_list(replica_hash_dict,source_hash_dict,log_file_path, 
                                updated_files,source_folder_path, log_list):
    #  Now we compare using the hashes to see whats been updated
    #  for files that have the same name and different hashes, we update the list of updated files
            for replica_name, replica_hash in replica_hash_dict.items(): 
                for source_name, source_hash in source_hash_dict.items():
                    if replica_name == source_name and replica_hash != source_hash and replica_name not in log_list:
                        write_to_log(source_name, log_file_path, "update")
                        #   might delete, this should help the log file
                        replica_hash_dict[source_name] = get_file_hash(os.path.join(source_folder_path,source_name), log_list)
                        updated_files.append(source_name)
                        log_list.append(source_name)
                        
def populate_added_files_list(source_folder_path,added_files,replica_folder_path,
                              log_file_path, log_list):
            # For each file in SOURCE that isn't yet in REPLICA, we add to the list of added files
            for file_name in os.listdir(source_folder_path):
                if file_name not in os.listdir(replica_folder_path) and file_name not in log_list:
                            added_files.append(file_name)
                            log_list.append(file_name)
                            write_to_log(file_name, log_file_path, "add")
                                                                           
def populate_removed_files_list(replica_folder_path,source_folder_path, 
                                removed_files,log_file_path,log_list):
            # For each file in the REPLICA that isnt in the SOURCE, this adds to the list of removed files        
            for file_name in os.listdir(replica_folder_path):
                file_path = os.path.join(replica_folder_path, file_name)
                if file_name not in os.listdir(source_folder_path) and file_name not in log_list:
                        removed_files.append(file_name)
                        log_list.append(file_name)
                        write_to_log(file_name, log_file_path, "remove")