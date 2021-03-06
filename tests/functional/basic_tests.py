from os import path, getenv, mkdir
import tempfile
import logging

from clustering_outliers.app import app


_tempdir: str = ""


def setup_module():
    print(f" == Setting up tests for {__name__}")
    app.config['TESTING'] = True

    global _tempdir
    _tempdir = getenv('TEMPDIR')
    if _tempdir:
        try:
            mkdir(_tempdir)
        except FileExistsError:
            pass
    else:
        _tempdir = tempfile.gettempdir()


def teardown_module():
    print(f" == Tearing down tests for {__name__}")


# Tests
dirname = path.dirname(__file__)
csv_file = path.join(dirname, '..', 'test_data', 'luxembourg-pois.osm.csv')
shp_file = path.join(dirname, '..', 'test_data', 'get_pois_v02_corfu_2100.zip')


def test_get_documentation_1():
    with app.test_client() as client:
        res = client.get('/', query_string=dict(), headers=dict())
        assert res.status_code == 200
        r = res.get_json()
        assert not (r.get('openapi') is None)


def test_get_health_check():
    with app.test_client() as client:
        res = client.get('/_health', query_string=dict(), headers=dict())
        assert res.status_code == 200
        r = res.get_json()
        if 'reason' in r:
            logging.error('The service is unhealthy: %(reason)s\n%(detail)s', r)
        logging.debug("From /_health: %s" % r)
        assert r['status'] == 'OK'


def test_file_kmeans_csv():
    payload = {'resource': (open(csv_file, 'rb'), 'sample.csv'), "resource_type": "csv", "id_column": "ID", "columns-0": "LON",
               "columns-1": "LAT"}
    with app.test_client() as client:
        res = client.post('/kmeans/file', data=payload, content_type='multipart/form-data')
        assert res.status_code == 200
        r = res.get_json()
        assert set(r.keys()) == {'cluster_centers', 'ids', 'labels'}


def test_file_kmeans_shp():
    payload = {'resource': (open(shp_file, 'rb'), 'sample.zip'), "resource_type": "shp"}
    with app.test_client() as client:
        res = client.post('/kmeans/file', data=payload, content_type='multipart/form-data')
        assert res.status_code == 200
        r = res.get_json()
        assert set(r.keys()) == {'cluster_centers', 'ids', 'labels'}


def test_path_kmeans_csv():
    payload = {"resource": csv_file, "resource_type": "csv", "id_column": "ID", "columns-0": "LON", "columns-1": "LAT"}
    with app.test_client() as client:
        res = client.post('/kmeans/path', data=payload, content_type='multipart/form-data')
        assert res.status_code == 200
        r = res.get_json()
        assert set(r.keys()) == {'cluster_centers', 'ids', 'labels'}


def test_path_kmeans_shp():
    payload = {"resource": shp_file, "resource_type": "shp"}
    with app.test_client() as client:
        res = client.post('/kmeans/path', data=payload, content_type='multipart/form-data')
        assert res.status_code == 200
        r = res.get_json()
        assert set(r.keys()) == {'cluster_centers', 'ids', 'labels'}


def test_file_dbscan_csv():
    payload = {'resource': (open(csv_file, 'rb'), 'sample.csv'), "resource_type": "csv", "id_column": "ID", "columns-0": "LON",
               "columns-1": "LAT"}
    with app.test_client() as client:
        res = client.post('/dbscan/file', data=payload, content_type='multipart/form-data')
        assert res.status_code == 200
        r = res.get_json()
        assert set(r.keys()) == {'core_sample_indices', 'components', 'ids', 'labels'}


def test_file_dbscan_shp():
    payload = {'resource': (open(shp_file, 'rb'), 'sample.zip'), "resource_type": "shp"}
    with app.test_client() as client:
        res = client.post('/dbscan/file', data=payload, content_type='multipart/form-data')
        assert res.status_code == 200
        r = res.get_json()
        assert set(r.keys()) == {'core_sample_indices', 'components', 'ids', 'labels'}


def test_file_agglomerative_csv():
    payload = {'resource': (open(csv_file, 'rb'), 'sample.csv'), "resource_type": "csv", "id_column": "ID", "columns-0": "LON",
               "columns-1": "LAT"}
    with app.test_client() as client:
        res = client.post('/agglomerative/file', data=payload, content_type='multipart/form-data')
        assert res.status_code == 200
        r = res.get_json()
        assert set(r.keys()) == {'n_clusters', 'n_leaves', 'n_connected_components', 'children', 'ids', 'labels'}


def test_file_agglomerative_shp():
    payload = {'resource': (open(shp_file, 'rb'), 'sample.zip'), "resource_type": "shp"}
    with app.test_client() as client:
        res = client.post('/agglomerative/file', data=payload, content_type='multipart/form-data')
        assert res.status_code == 200
        r = res.get_json()
        assert set(r.keys()) == {'n_clusters', 'n_leaves', 'n_connected_components', 'children', 'ids', 'labels'}


def test_file_isolation_forest_csv():
    payload = {'resource': (open(csv_file, 'rb'), 'sample.csv'), "resource_type": "csv", "id_column": "ID", "columns-0": "LON",
               "columns-1": "LAT"}
    with app.test_client() as client:
        res = client.post('/isolation_forest/file', data=payload, content_type='multipart/form-data')
        assert res.status_code == 200
        r = res.get_json()
        assert isinstance(r, dict)


def test_file_isolation_forest_shp():
    payload = {'resource': (open(shp_file, 'rb'), 'sample.zip'), "resource_type": "shp"}
    with app.test_client() as client:
        res = client.post('/isolation_forest/file', data=payload, content_type='multipart/form-data')
        assert res.status_code == 200
        r = res.get_json()
        assert isinstance(r, dict)


def test_file_local_outlier_factor_csv():
    payload = {'resource': (open(csv_file, 'rb'), 'sample.csv'), "resource_type": "csv", "id_column": "ID", "columns-0": "LON",
               "columns-1": "LAT"}
    with app.test_client() as client:
        res = client.post('/local_outlier_factor/file', data=payload, content_type='multipart/form-data')
        assert res.status_code == 200
        r = res.get_json()
        assert isinstance(r, dict)


def test_file_local_outlier_factor_shp():
    payload = {'resource': (open(shp_file, 'rb'), 'sample.zip'), "resource_type": "shp"}
    with app.test_client() as client:
        res = client.post('/local_outlier_factor/file', data=payload, content_type='multipart/form-data')
        assert res.status_code == 200
        r = res.get_json()
        assert isinstance(r, dict)


def test_file_one_class_svm_csv():
    payload = {'resource': (open(csv_file, 'rb'), 'sample.csv'), "resource_type": "csv", "id_column": "ID", "columns-0": "LON",
               "columns-1": "LAT"}
    with app.test_client() as client:
        res = client.post('/one_class_svm/file', data=payload, content_type='multipart/form-data')
        assert res.status_code == 200
        r = res.get_json()
        assert isinstance(r, dict)


def test_file_one_class_svm_shp():
    payload = {'resource': (open(shp_file, 'rb'), 'sample.zip'), "resource_type": "shp"}
    with app.test_client() as client:
        res = client.post('/one_class_svm/file', data=payload, content_type='multipart/form-data')
        assert res.status_code == 200
        r = res.get_json()
        assert isinstance(r, dict)
