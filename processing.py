'''
Contains all the helper functions that talk about
'''

from nltk.tokenize import sent_tokenize, word_tokenize
import re
from datasets.most_common_words import most_common_words
from datasets.programming_syntax import programming_syntax

def generate_token(test_file_path):

    tokens = []
    has_chars = re.compile(r"[\w|\d]", re.IGNORECASE)
    regexp_quotes = re.compile(r"^['(\[\"]|[\"'\])]$", re.IGNORECASE)

    with open(test_file_path, 'r', encoding='utf8') as test_file:
        file_text = test_file.read()
        # Replaces escape character with space
        final = file_text.replace("\n", " ")
        for i in sent_tokenize(final):
            temp = []
            
            # tokenize the sentence into words
            for j in word_tokenize(i):

                # PreProcess here
                if (has_chars.search(j)):
                    processed = regexp_quotes.sub("", j.lower())
                    temp.append(processed)
        
            tokens.append(temp)

        # Flat the array
        tokens = [item for sublist in tokens for item in sublist]

        # Rid duplicates
        tokens = list(set(tokens))

    return tokens

def filter_words():
    return list(sorted(programming_syntax() + most_common_words()))

def bin_search(token):
    '''
    Performs a binary search and tells us if a token exists in filter_words
    '''
    filter_arr = filter_words()

    left = 0
    right = len(filter_arr) - 1
    mid = 0

    while (left < right):
        mid = (left + right) // 2

        if (filter_arr[mid] == token):
            return True
        elif (filter_arr[mid] > token):
            right = mid - 1
        else:
            left = mid + 1
    
    return False

# Logic is that some programmers name their variables weirdly so you also capture variables like 'cdf' or 'rsk' that make no sense
def filter_length(token):
    '''
    Return whether or not a token passes the filter length
    '''

    FILTER_LENGTH = 7

    if isinstance(token, (int, float)):
        return False
    return len(token) > FILTER_LENGTH

if __name__ == '__main__':
    pass