import processing
import os
import datasets.most_common_words as most_common_words
import datasets.api_keys as api_keys

def iter_dir(path: str):

    # Step 1: Tokenize
    tokens = []

    for filename in os.listdir(path):
        f = os.path.join(path, filename)
        if os.path.isfile(f):
            tokens += processing.generate_token(f)

    tokens = list(filter(lambda token: processing.filter_length(token) and (not processing.bin_search(token))), tokens)

    non_api_keys = most_common_words()[:len(api_keys())]

    ### Step 4: Creation of Classifier Model
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.model_selection import train_test_split

    # Create labels
    y_api = [1] * len(api_keys)
    y_non_api = [0] * len(non_api_keys)

    # Combine data
    X = api_keys + non_api_keys
    y = y_api + y_non_api

    # Convert text data into numerical vectors
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(2,2))
    X_vectorized = vectorizer.fit_transform(X)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)

    # Train a Random Forest Classifier
    clf = RandomForestClassifier(n_estimators=30)
    clf.fit(X_train, y_train)

    # Test the model
    # Wow it's like 0.96 accuracy
    # print("Model Accuracy: ", clf.score(X_test, y_test))

    # print(clf.predict(vectorizer.transform(["3n2Q4G9BbDnar73lbU/LPQ==6MoLMcahNldNAxET"])))

    # Run the predictor model
    found_api_keys = []
    for token in tokens:
        if clf.predict(vectorizer.transform([token])) == [1]:
            found_api_keys.append(token)

    return found_api_keys


if __name__ == '__main__':
    pass