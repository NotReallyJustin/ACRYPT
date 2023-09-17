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

def commit(message):
    assert message != None, "You must provide a commit message"

    # Thought about making a try catch, but the github error messages are more precise
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
    encrypted_api_keys = list(map(lambda api_key: encryption(api_key, key), found_api_keys))

    if (not nocommit):
        commit(message)
        encryption.decrypt()

    # Create a .decrypt file and add it to .gitignore
    with open(".gitignore", "a", encoding="utf8") as gitignore:
        gitignore.write(".decrypt")
    
    with open(".decrypt", "w", encoding="uft8") as decrypt_file:
        decrypt_file.write()

def undo_acrypt():
    '''
    Decrypts an instance of ACRYPT.
    Requires a .decrypt file that you give to people you want to have access to API key
    '''

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