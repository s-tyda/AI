import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam

df = pd.read_csv('resources/weather_madrid_LEMD_1997_2015.csv')

df[' Events'] = df[' Events'].fillna('Nothing')
df['Month'] = [x.month for x in pd.to_datetime(df['CET'])]
df = df.drop(columns=['CET'])

X = df.drop([' Events'], axis=1)
X = X.fillna(X.median())
Y = df[' Events']
Y = pd.get_dummies(Y).astype('int')

scaler = MinMaxScaler()
X = scaler.fit_transform(X)

scores = []
for i in range(100):
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.8)

    model = Sequential()
    model.add(Dense(X.shape[1], input_shape=(X.shape[1],), activation='linear'))
    model.add(Dropout(0.20))
    model.add(Dense(32, activation='sigmoid'))
    model.add(Dropout(0.20))
    model.add(Dense(64, activation='sigmoid'))
    model.add(Dropout(0.20))
    model.add(Dense(32, activation='sigmoid'))
    model.add(Dropout(0.20))
    model.add(Dense(Y.shape[1], activation='softmax'))

    model.compile(optimizer=Adam(lr=0.01),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(x=X_train,
              y=Y_train,
              epochs=200,
              validation_split=0.20,
              callbacks=[EarlyStopping(monitor='loss', patience=5)])

    predictions = model.predict(X_test)
    score = accuracy_score(Y_test.values.argmax(axis=1),
                           predictions.argmax(axis=1))

    scores.append(score)
    print(f'Accuracy: {round(score * 100, 2)}%\n')
    print(confusion_matrix([np.argmax(x) for x in Y_test.values], [np.argmax(x) for x in predictions]), end='\nn')
    print(classification_report([np.argmax(x) for x in Y_test.values], [np.argmax(x) for x in predictions]))

print(f'Min accuracy: {round(min(scores) * 100, 2)}%\n')
print(f'Avg accuracy: {round((sum(scores)/len(scores)) * 100, 2)}%\n')
print(f'Max accuracy: {round(max(scores) * 100, 2)}%\n')
