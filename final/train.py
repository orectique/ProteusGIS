import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def add_data(data):
    df = pd.read_csv('historicalData2.csv')

    df.loc[len(df)] = data

    df.to_csv('historicalData2.csv', index=False)

    return df

def train_model(data):
    X = data[[]]