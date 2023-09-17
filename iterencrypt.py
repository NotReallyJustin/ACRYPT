import os
from datasets.exclusion import file_to_exclude, folders_to_exclude

def is_substring(str, list):
    '''
    Given a string and a list, return whether anything in the list is a substring of str
    '''

    for item in list:
        if item in str:
            return True
    return False

def iter_encrypt_fernet(path:str, found_api_keys:str, encrypted_api_keys:str):
    '''
    Iterates through the path recursively, and replace found API keys with their encrypted one
    '''
    for (root, dirs, file_names) in os.walk(path):
        for file_name in file_names:
            if ((file_name not in file_to_exclude()) and (not is_substring(root, folders_to_exclude()))):
                file_path = os.path.join(root, file_name)
                
                with open(file_path, 'w+', encoding="utf8") as file:
                    file_code = file.read()
                    
                    # Doesn't matter which we iterate as found_api_keys[i] --> encrypted_api_keys[i]
                    for i in range(len(encrypted_api_keys)):
                        file_code = file_code.replace(found_api_keys[i], encrypted_api_keys[i])
                    
                    file.write(file_code)

def iter_encrypt_fernet(path:str, encrypted_api_keys:str, decrypted_api_keys:str):
    '''
    Iterates through the path recursively, and replace found encrypted API keys with decrypted counterparts
    '''
    iter_encrypt_fernet(path, encrypted_api_keys, decrypted_api_keys)