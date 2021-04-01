import json

import pandas as pd
import fiona
from kneed import KneeLocator
from shapely.geometry import mapping, asShape
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from ..forms import BaseKMeansForm
from ..utils import get_delimiter, has_header


def kmeams(form: BaseKMeansForm, file_path: str):
    file_type: str = form.resource_type.data
    ids: list = []
    if file_type == 'csv':
        delimiter = get_delimiter(file_path)
        header = has_header(file_path)
        if header:
            column_names = []
            column_names.append(form.id_column_name.data)
            for name in form.column_names.data:
                column_names.append(name)
            data = pd.read_csv(file_path, delimiter=delimiter, header=0, usecols=column_names)
            ids = data[[column_names[0]]].values.tolist()
            del data[column_names[0]]
        else:
            column_numbers = []
            column_numbers.append(form.id_column_number.data)
            for number in form.column_numbers.data:
                column_numbers.append(number)
            data = pd.read_csv(file_path, delimiter=delimiter, header=None, usecols=column_numbers)
            ids = data[[column_numbers[0]]].values.tolist()
            del data[column_numbers[0]]
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
        kmeans.fit(scaled_features)
        sse.append(kmeans.inertia_)

    kl = KneeLocator(
        range(1, 11), sse, curve="convex", direction="decreasing"
    )

    k = kl.elbow

    # Initilize and run kMeans clustering
    kmeans = KMeans(
        init="random",
        n_clusters=k,
        n_init=10,
        max_iter=300,
        random_state=42
    )
    kmeans.fit(scaled_features)

    # The results are the cluster centers and element membership
    centers = []
    for center in kmeans.cluster_centers_:
        centers.append(center.tolist())
    response = {
        "cluster_centers": json.dumps(centers),
        "ids": ids,
        "labels": json.dumps(kmeans.labels_.tolist()),
    }
    return response
