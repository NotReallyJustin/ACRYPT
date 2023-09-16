'''
Entry Point of main.py
Basically the "CLI interface" you see
'''

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Initiates ACRYPT to encrypt all API keys and then commit changes.')
    parser.add_argument('-m', '--manual', help='Do not commit changes', action='store_true')
    parser.add_argument('-u', '--undo', help='Undo an instance of ACRYPT', action='store_true')

    flags = vars(parser.parse_args())

    print(flags)