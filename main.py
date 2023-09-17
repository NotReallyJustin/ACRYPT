'''
Entry Point of main.py
Basically the "CLI interface" you see
@author Amartya Kalra & Justin Chen
'''

import argparse
import os
import encryption
import fernet
from classifier import iter_dir
import iterencrypt

def commit(message, path="./"):
    assert message != None, "You must provide a commit message"

    # Thought about making a try catch, but the github error messages are more precise
    os.system(f"cd {path}")
    os.system("git add -A")
    os.system(f"git commit -a -m {message}")

def run_acrypt(message:str, nocommit:bool, path:str):
    '''
    Runs ACRYPT. Then commits the changes depending on whether or not the user flagged nocommit
    @param message Commit Message
    @param nocommit Whether or not to commit
    '''
    if path == None:
        path = "./"

    key = fernet.generateKey()
    found_api_keys = iter_dir(path)
    encrypted_api_keys = list(map(lambda api_key: fernet.encryption(api_key, key), found_api_keys))

    if (not nocommit):
        iterencrypt.iter_encrypt_fernet(path, found_api_keys, encrypted_api_keys)
        commit(message)

        decrypted_api_keys = list(map(lambda enc_key: fernet.decryption(enc_key, key), encrypted_api_keys))
        iterencrypt.iter_decrypt_fernet(path, encrypted_api_keys, decrypted_api_keys)
    else:
        # Create a .decrypt file and add it to .gitignore
        gitignore_path = os.path.join(path, ".gitignore")
        with open(gitignore_path, "a", encoding="utf8") as gitignore:
            gitignore.write(".decrypt")
        
        decrypt_path = os.path.join(path, ".decrypt")
        with open(decrypt_path, "w", encoding="uft8") as decrypt_file:
            to_write = key

            for i in encrypted_api_keys:
                to_write += f"\n{i}"
            decrypt_file.write(to_write)

    print("ACRYPT Completed.")

def undo_acrypt(path:str):
    '''
    Decrypts an instance of ACRYPT.
    Requires a .decrypt file that you give to people you want to have access to API key
    '''
    decrypt_path = os.path.join(path, ".decrypt")
    if os.path.isfile(decrypt_path):
        with open(decrypt_path, "r", encoding="uft8") as decrypt_file:
            try:
                decrypt_arr = decrypt_file.read().split("\n")
                key = decrypt_arr[0]
                encrypted_api_keys = decrypt_arr[1:]
            except:
                print("Invalid .decrypt file")
                return
            
            decrypted_api_keys = list(map(lambda enc_key: fernet.decryption(enc_key, key), encrypted_api_keys))

            iterencrypt.iter_decrypt_fernet(path, encrypted_api_keys, decrypted_api_keys)
        print("ACRYPT Undone.")
    else:
        print(".decrypt file not found. Cannot undo encryption. Make sure you're in the proper root directory.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Initiates ACRYPT to encrypt all API keys and then commit changes.')
    parser.add_argument('-m', '--message', help="Commit message")
    parser.add_argument('-n', '--nocommit', help='Do not commit changes', action='store_true')
    parser.add_argument('-d', '--decrypt', help='Decrypt/Undo an instance of ACRYPT', action='store_true')
    parser.add_argument('-p', '--path', help="Path to run ACRYPT. If not specified, this defaults to current directory")

    flags = vars(parser.parse_args())

    if (flags.decrypt):
        undo_acrypt()
    else:
        run_acrypt(flags.message, flags.nocommit, flags.path)