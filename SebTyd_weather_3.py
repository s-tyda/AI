import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from imblearn.over_sampling import RandomOverSampler


def print_score(y_test, y_pred, classes):
    print(model.__class__.__name__)

    scores = {}
    for single_class in classes:
        scores[single_class] = np.zeros(len(classes))
    scores = pd.DataFrame(scores)

    for idx, val in enumerate(list(y_test)):
        scores[str(val)][y_pred[idx]] += 1

    print(scores.to_string())


df = pd.read_csv('resources/weather_madrid_LEMD_1997_2015.csv')

df[' Events'] = df[' Events'].fillna('Clean')
df['Month'] = [x.month for x in pd.to_datetime(df['CET'])]
df = df.drop(columns=['CET'], axis=1)

classes = list(df.groupby(' Events').count().index)

X = df.drop([' Events'], axis=1)
X = X.fillna(X.median())
Y = df[' Events']
scaler = MinMaxScaler()
X = scaler.fit_transform(X)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.8)
model = KMeans(n_clusters=len(classes), init='k-means++', max_iter=100)
model.fit(X_train, Y_train)
Y_pred = model.predict(X_test)

print_score(Y_test, Y_pred, classes)

