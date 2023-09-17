import processing
import os
from datasets.most_common_words import most_common_words
from datasets.api_keys import api_keys
from datasets.exclusion import file_to_exclude, folders_to_exclude

def is_substring(str, list):
    '''
    Given a string and a list, return whether anything in the list is a substring of str
    '''

    for item in list:
        if item in str:
            return True
    return False

def iter_dir(path: str):

    # Step 1: Tokenize
    tokens = []
    non_lower_tokens = []

    for (root, dirs, file_names) in os.walk(path):
        for file_name in file_names:
            if ((file_name not in file_to_exclude()) and (not is_substring(root, folders_to_exclude()))):
                file_path = os.path.join(root, file_name)

                (a, b) = processing.generate_token(file_path)
                tokens += a
                non_lower_tokens += b

    # Step 2/3: Pre-process filtering
    tokens = list(filter(lambda token: processing.filter_length(token) and (not processing.bin_search(token)), tokens))
    non_lower_tokens = list(filter(lambda token: processing.filter_length(token), non_lower_tokens))

    ### Step 4: Creation of Classifier Model
    non_api_keys = most_common_words()[:len(api_keys())]

    from sklearn.ensemble import RandomForestClassifier
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.model_selection import train_test_split

    # Create labels
    y_api = [1] * len(api_keys())
    y_non_api = [0] * len(non_api_keys)

    # Combine data
    X = api_keys() + non_api_keys
    y = y_api + y_non_api

    # Convert text data into numerical vectors
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(2,2))
    X_vectorized = vectorizer.fit_transform(X)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)

    # Train a Random Forest Classifier
    clf = RandomForestClassifier(n_estimators=50)
    clf.fit(X_train, y_train)

    # Test the model
    # Wow it's like 0.92 accuracy
    # print("Model Accuracy: ", clf.score(X_test, y_test))

    # \\print(clf.predict(vectorizer.transform(["3n2Q4G9BbDnar73lbU/LPQ==6MoLMcahNldNAxET"])))

    # Run the predictor model
    found_api_keys = []
    for token in tokens:
        if clf.predict(vectorizer.transform([token])) == [1]:
            found_api_keys.append(token)

    # Step 6: Account for upper/lower case
    to_ret_keys = []

    for i in non_lower_tokens:
        if i.lower() in found_api_keys:
            to_ret_keys.append(i)

    return to_ret_keys


if __name__ == '__main__':
    #print(iter_dir("../BasicWeatherApp/"))
    pass