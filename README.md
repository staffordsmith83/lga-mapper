# Setup
```
pip install -r requirements.txt

# Need to also set env variables for DB username and password like this:
export DB_USERNAME="############"
export DB_PASSWORD="############"
export FLASK_ENV=development

# to run on port 5000
flask run
# or to run on port of your choice
flask run -h localhost -p 5001
```

You will also need to have postgres installed and running.
Create a database called `postgres` and install the PostGIS extension
That db name is defined in each endpoint currently...
Need to have a schema called `api` and within that a table called `lgas`
Currently this table is imported from the shapefile here: https://data.peclet.com.au/api/explore/v2.1/catalog/datasets/nsw-lga-boundaries/exports/shp?lang=en&timezone=Australia%2FSydney
Or if that doesnt work the parent page here:
https://data.peclet.com.au/explore/dataset/nsw-lga-boundaries/export/


## Notes

To get all lgas can do

http://localhost:5000/lgas


To get one LGA for a provided lat and lng can do
http://127.0.0.1:5000/lga?lat=-29.123&lng=149.694

Note the difference between the endpoints `lgas` and `lga`