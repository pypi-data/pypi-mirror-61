import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

class TitanicTestowy():
    def __init__(self, file_or_buffer):
        self.file_or_buffer = file_or_buffer
        self.predictions = np.zeros(1)

    def preprocessing(self):
        df = pd.read_csv(self.file_or_buffer, sep='\t')
        df['Cabin'] = df['Cabin'].fillna('empty')
        df['Age'] = df['Age'].fillna(df['Age'].mean())
        df['CabinLevel'] = np.where(df['Cabin'] != 'empty', df['Cabin'].str[0], 'empty')
        df = df.drop(['Name', 'Ticket', 'Cabin'], axis=1)
        df = pd.get_dummies(df)
        return df

    def get_predictions(self):
        df = self.preprocessing()
        self.y = df['Survived']
        self.X = df.drop(['Survived'], axis=1)
        model = LogisticRegression(solver='lbfgs', max_iter=500)
        model.fit(self.X, self.y)
        return model.predict(self.X)

    def get_score_recall(self):
        self.predictions = self.get_predictions()
        return accuracy_score(self.y, self.predictions)


if __name__ == '__main__':
    test = TitanicTestowy(r'c:/Users/gromim01/titanic.csv')
    print(test.get_score_recall())
    print(test.preprocessing())