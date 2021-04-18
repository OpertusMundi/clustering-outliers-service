import fiona
from flask_wtf import FlaskForm
import pandas as pd
from kneed import KneeLocator
from shapely.geometry import mapping, asShape
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from ..utils import get_delimiter, has_header


def get_dataframe(form: FlaskForm, file_path: str):
    file_type: str = form.resource_type.data
    ids: list = []
    if file_type == 'csv':
        delimiter = get_delimiter(file_path)
        header = has_header(file_path)
        columns = [form.id_column.data]
        if header:
            for name in form.columns.data:
                columns.append(name)
            data = pd.read_csv(file_path, delimiter=delimiter, header=0, usecols=columns)
        else:
            for number in form.columns.data:
                columns.append(number)
            data = pd.read_csv(file_path, delimiter=delimiter, header=None, usecols=columns)
        ids = data[[columns[0]]].values.tolist()
        del data[columns[0]]
    elif file_type == 'shp':
        ids = []
        data = []
        with fiona.open(file_path) as src:
            for el in src:
                lat = mapping(asShape(el['geometry']).centroid)['coordinates'][0]
                lon = mapping(asShape(el['geometry']).centroid)['coordinates'][1]
                data.append([lat, lon])
                ids.append(el['id'])
            data = pd.DataFrame(data, columns=['LAT', 'LON'])
    # Normalize the data
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(data)
    return scaled_features, ids


def get_kmeans_k(features):
    # Determine optimal number of clusters using Elbow point
    kmeans_kwargs = {
        "init": "random",
        "n_init": 10,
        "max_iter": 300,
        "random_state": 42,
    }
    # A list holds the SSE values for each k
    sse = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(features)
        sse.append(kmeans.inertia_)

    kl = KneeLocator(
        range(1, 11), sse, curve="convex", direction="decreasing"
    )

    return kl.elbow
