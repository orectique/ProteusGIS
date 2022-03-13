from flask import Flask
from flask_restful import Resource, Api, reqparse
from joblib import dump, load
from datetime import datetime
import numpy as np

from leslieDelury import popEstimate

import pandas as pd

app = Flask(__name__)
api = Api(app)

dictVals = {
    'year' : 2022, 'month': 2, 'day': 14, 'time': 1, 'species_1': 0,
       'species_10': 0, 'species_11': 0, 'species_12': 0,
       'species_13': 0, 'species_2': 0, 'species_3': 0,
       'species_4': 0, 'species_5': 0, 'species_6': 0,
       'species_7': 0, 'species_8': 0, 'species_9': 0,
       'location_AB1': 0, 'location_AB2': 0, 'location_AB3': 0, 'location_C1': 0,
       'location_C2': 0, 'location_C3': 0, 'location_E': 0, 'location_H1': 0,
       'location_H2': 0, 'location_H3': 0, 'location_H4': 0, 'location_H5': 0,
       'location_H6': 0, 'location_MBA': 0
}

dictInput = {
    'date' : 0, 'time': 0, 'catch': 0, 'effort' : 0, 'boat': 0, 'species_' : 0, 'location_': 0, 'species_1': 0,
       'species_10': 0, 'species_11': 0, 'species_12': 0,
       'species_13': 0, 'species_2': 0, 'species_3': 0,
       'species_4': 0, 'species_5': 0, 'species_6': 0,
       'species_7': 0, 'species_8': 0, 'species_9': 0,
       'location_AB1': 0, 'location_AB2': 0, 'location_AB3': 0, 'location_C1': 0,
       'location_C2': 0, 'location_C3': 0, 'location_E': 0, 'location_H1': 0,
       'location_H2': 0, 'location_H3': 0, 'location_H4': 0, 'location_H5': 0,
       'location_H6': 0, 'location_MBA': 0
}

locations = ['location_AB1', 'location_AB2', 'location_AB3', 'location_C1',
       'location_C2', 'location_C3', 'location_E', 'location_H1',
       'location_H2', 'location_H3', 'location_H4', 'location_H5',
       'location_H6', 'location_MBA']

coordinates = {
    'location_AB1': (9.893443, 76.113282), 'location_AB2': (9.895726, 76.115385), 'location_AB3': (9.918204, 76.188637), 'location_C1': (9.943952, 76.157352),
       'location_C2': (9.896554, 76.181639), 'location_C3': (9.979392, 76.081605), 'location_E': (9.795376, 76.220591), 'location_H1': (9.744776, 76.124983),
       'location_H2': (9.930564, 75.884192), 'location_H3': (9.869518, 76.160393), 'location_H4': (9.952363, 76.208197), 'location_H5': (9.896554, 76.157737),
       'location_H6': (9.839863, 76.201115), 'location_MBA': (9.893066, 76.168361)
}

species = ['species1', 'species10', 'species11', 'species12', 'species13',
       'species2', 'species3', 'species4', 'species5', 'species6',
       'species7', 'species8', 'species9']

X_list = ['year', 'month', 'day', 'time', 'species_1', 'species_10', 'species_11', 'species_12', 'species_13',
       'species_2', 'species_3', 'species_4', 'species_5', 'species_6',
       'species_7', 'species_8', 'species_9',
       'location_AB1', 'location_AB2', 'location_AB3', 'location_C1',
       'location_C2', 'location_C3', 'location_E', 'location_H1',
       'location_H2', 'location_H3', 'location_H4', 'location_H5',
       'location_H6', 'location_MBA']
y_list = ['catch']

class Predict(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('date', required = True)
        parser.add_argument('time', required = True)
        parser.add_argument('species', required = True)

        args = parser.parse_args()

        output = pd.DataFrame(columns=['loc', 'species', 'catch'])

        spec = args['species']

        clf = load('MLPreg.joblib')

        body = dictVals.copy()

        date = datetime.strptime(args['date'], '%Y-%m-%d')

        body['year'] = int(date.year)
        body['month'] = int(date.month)
        body['day'] = int(date.day)
        body['time'] = args['time']

        for loc in locations:
            k = body.copy()

            k[loc] = 1
            k[spec] = 1

            l = pd.DataFrame(k, index = [0])
            print(l)
        
            output.loc[len(output)] = [loc, spec, clf.predict(l)[0]]
            output['catch'] = output['catch'].astype(int)
        
        ideal_loc = output[output['catch'] == output.catch.max()]

        loc = ideal_loc['loc'].values
        spec = ideal_loc['species'].values

        catch = ideal_loc['catch'].values
        
        geo_loc = coordinates[loc[0]]

        out =  {
            'location': loc[0],
            'species': spec[0],
            'catch': int(catch[0]),
            'latitude': geo_loc[0],
            'longitude': geo_loc[1]
        }
    
        return out, 200

class Update(Resource):
    def __init__(self):
        self.buffer = pd.DataFrame(columns=['date', 'time', 'catch', 'effort', 'boat', 'species_', 'location_',
       'species_1', 'species_10', 'species_11', 'species_12', 'species_13',
       'species_2', 'species_3', 'species_4', 'species_5', 'species_6',
       'species_7', 'species_8', 'species_9', 'location_AB1', 'location_AB2',
       'location_AB3', 'location_C1', 'location_C2', 'location_C3',
       'location_E', 'location_H1', 'location_H2', 'location_H3',
       'location_H4', 'location_H5', 'location_H6', 'location_MBA', 'year',
       'month', 'day'])

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('date', required = True)
        parser.add_argument('time', required = True)
        parser.add_argument('species', required = True)
        parser.add_argument('boat', required = True)
        parser.add_argument('catch', required = True)
        parser.add_argument('effort', required = True)
        parser.add_argument('loc', required = True)

        args = parser.parse_args()

        body = dictVals.copy()

        date = datetime.strptime(args['date'], '%Y-%m-%d')

        body['date'] = args['date']
        body['year'] = int(date.year)
        body['month'] = int(date.month)
        body['day'] = int(date.day)
        body['time'] = int(args['time'])
        body['catch'] = int(args['catch'])
        body['effort'] = int(args['effort'])
        body['boat'] = args['boat']
        body['species_'] = args['species'].replace('_', '')
        body['location_'] = args['loc']

        body[args['species']] = 1
        body['location_' + args['loc']] = 1

        self.buffer = self.buffer.append(body, ignore_index=True)

        if len(self.buffer) < 30:
            return 'Data added to corpus', 200  
            
        else:        
            corpus = pd.read_csv('historicalDataTrain.csv')
            corpus = corpus.append(self.buffer, ignore_index=True)
            corpus.to_csv('historicalDataTrain.csv', index = False)

            X = corpus[X_list]
            y = corpus[y_list]

            reg = load('MLPreg.joblib')

            reg.fit(X, y)

            dump(reg, 'MLPreg.joblib')

            self.buffer = self.buffer.drop(self.buffer.index, inplace = True)

            return 'Data added and trained', 200        

class Estimate(Resource):
    def get(self):    
        corpus = pd.read_csv('historicalDataTrain.csv')

        now = datetime(2022, 1, 1)

        year = int(now.year)
        month = int(now.month)

        if month == 1:
            year -= 1
            month = 12
        
        corpus = corpus[(corpus['year'] == year) & (corpus['month'] == month)]

        output = pd.DataFrame(columns = ['species', 'estimate'])

        for spec in species:
            temp = corpus[corpus['species_'] == spec]

            if len(temp) == 0:
                estimate = 'N/A'
                
            else:
                estimate, val = popEstimate.LDEstimate(temp['catch'].values, temp['effort'].values)

                if estimate < 0 or np.isnan(estimate):
                    estimate = 'N/A'
                else:
                    estimate = int(estimate)

            output.loc[len(output)] = [spec, estimate]

        output = output.set_index('species')

        output = output.to_dict()

        return output, 200    
    

api.add_resource(Predict, '/predict')
api.add_resource(Update, '/update')
api.add_resource(Estimate, '/estimate')

if __name__ == "__main__":
    app.run(debug = True)