'''
Entry Point of main.py
Basically the "CLI interface" you see
@author Amartya Kalra & Justin Chen
'''

import argparse
import os

def commit(message):
    assert message != None, "You must provide a commit message"
    os.system("git add -A")
    os.system(f"git commit -a -m {message}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Initiates ACRYPT to encrypt all API keys and then commit changes.')
    parser.add_argument('-m', '--message', help="Commit message")
    parser.add_argument('-n', '--nocommit', help='Do not commit changes', action='store_true')
    parser.add_argument('-u', '--undo', help='Undo an instance of ACRYPT', action='store_true')

    flags = vars(parser.parse_args())

    print(flags)