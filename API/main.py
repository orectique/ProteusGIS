from flask import Flask
from flask_restful import Resource, Api, reqparse
from joblib import dump, load
from datetime import datetime

import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

dictVals = {
    'year' : 2022, 'month': 2, 'day': 14, 'time': 1, 'species_species1': 0,
       'species_species10': 0, 'species_species11': 0, 'species_species12': 0,
       'species_species13': 0, 'species_species2': 0, 'species_species3': 0,
       'species_species4': 0, 'species_species5': 0, 'species_species6': 0,
       'species_species7': 0, 'species_species8': 0, 'species_species9': 0,
       'location_AB1': 0, 'location_AB2': 0, 'location_AB3': 0, 'location_C1': 0,
       'location_C2': 0, 'location_C3': 0, 'location_E': 0, 'location_H1': 0,
       'location_H2': 0, 'location_H3': 0, 'location_H4': 0, 'location_H5': 0,
       'location_H6': 0, 'location_MBA': 0
}

locations = ['location_AB1', 'location_AB2', 'location_AB3', 'location_C1',
       'location_C2', 'location_C3', 'location_E', 'location_H1',
       'location_H2', 'location_H3', 'location_H4', 'location_H5',
       'location_H6', 'location_MBA']

class Predict(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('date', required = True)
        parser.add_argument('time', required = True)
        parser.add_argument('species', required = True)

        args = parser.parse_args()

        output = pd.DataFrame(columns=['loc', 'species', 'catch'])

        spec = args['species']

        clf = load('rtclf.joblib')

        body = dictVals.copy()

        date = datetime.strptime(args['date'], format = '%Y-%m-%d')

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
        
        ideal_loc = output[output['catch'] == output.catch.max()].to_dict

        return {'data' : ideal_loc}, 200



        


class Estimate(Resource):
    pass

api.add_resource(Predict, '/predict')
api.add_resource(Estimate, '/estimate')

if __name__ == "__main__":
    app.run(debug = True)