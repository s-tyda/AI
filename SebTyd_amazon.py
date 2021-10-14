import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn import metrics


def score(model, y_test, predictions):
    print(f'{model.__class__.__name__} : {metrics.accuracy_score(y_test, predictions)}')
    print(metrics.classification_report(y_test, predictions))
    print(metrics.confusion_matrix(y_test, predictions))
    print()


df = pd.read_csv('resources/train-amazon.tsv', sep='\t')
X = df['review']
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

tests = ['Bad product',
         'Good product',
         'Tomasz approved',
         'Everything gone wrong',
         'I ordered something else',
         'OMG what a shit',
         'What the fuck is this?',
         'Im really excited about this thing, definietely buy it again in the future',
         'Fast shipment',
         '+1']

models = [LinearSVC(C=1.7), MultinomialNB(), RandomForestClassifier()]
for model in models:
    text_clf = Pipeline([('tfidf', TfidfVectorizer(min_df=2, max_df=0.46, ngram_range=(1, 2))), ('clf', model)])
    text_clf.fit(X_train, y_train)
    predictions = text_clf.predict(X_test)
    score(model, y_test, predictions)

    print("Tests:")
    predictions = text_clf.predict(tests)
    for test, prediction in zip(tests, predictions):
        print(test, "|", prediction)
    print()
