from kmeans.kmeans.app import app
import json
from os import path

def setup_module():
    app.config['TESTING'] = True
    pass

def teardown_module():
    pass

# Tests
dirname = path.dirname(__file__)
csv_file = path.join(dirname, '..', 'test_data', 'luxembourg-pois.osm.csv')
shp_file = path.join(dirname, '..', 'test_data', 'natura.shp')

def test_kmeans_csv():
    with app.test_client() as client:
        arguments = {"src_file": csv_file, "header": True, "id_column_name": "ID", "column_names": ["LON", "LAT"], "delimiter": "|"}
        res = client.post('/kmeans', json=json.dumps(arguments))
        print(res.status_code)
        assert res.status_code == 200
        r = res.get_json();
        print(r)

def test_kmeans_shp():
    with app.test_client() as client:
        arguments = {"src_file": shp_file}
        res = client.post('/kmeans', json=json.dumps(arguments))
        print(res.status_code)
        assert res.status_code == 200
        r = res.get_json();
        print(r)

# Test kMeans
test_kmeans_csv()
#test_kmeans_shp()