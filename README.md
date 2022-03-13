# Proteus

An API for geospatial prediction of fishing grounds. Just clone the repo and run main.py locally. I need sleep and will fix the Heroku issues in a bit.

### https://proteussih.herokuapp.com/predict

**method : GET**

date: yyyy-mm-dd  
time: 1, 2, 3, 4    
species: e.g. species_1

### https://proteussih.herokuapp.com/update

**method : POST**

date: yyyy-mm-dd  
time: 1, 2, 3, 4  
species: e.g. species_1  
boat: e.g. boat5  
catch: int  
effort: int  
loc: e.g. H2

### https://proteussih.herokuapp.com/estimate

**method : GET**
