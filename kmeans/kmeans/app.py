import logging
import urllib
import json
import pickle
import numpy as np
import pandas as pd

import fiona
from os import path
from shapely.geometry import mapping, asShape

from flask import Flask
from flask import request, session, current_app
from flask import url_for, make_response, redirect, abort
from flask import render_template

import matplotlib.pyplot as plt
from kneed import KneeLocator
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

@app.route("/")
def hello():
    response = make_response("Welcome to Topio's kMeans Clustering Service", 200);
    return response;

@app.route("/kmeans", methods=["POST"])
def kmeans():
    current_app.logger.info("Running kMeans...")

    # Get arguments and read from file
    if request.json is not None:
        arguments = json.loads(request.json)
        src_file = arguments['src_file']
        extension = path.splitext(src_file)[1]
        if extension == '.csv':
            has_header = arguments['header']
            delimiter = arguments['delimiter']
            if has_header == True:
                column_names = []
                column_names.append(arguments['id_column_name'])
                for name in arguments['column_names']:
                    column_names.append(name)
                data = pd.read_csv(src_file, delimiter=delimiter, header=0, usecols=column_names)
                ids = data[[column_names[0]]].values.tolist()
                del data[column_names[0]]
            else:
                column_numbers = []
                column_numbers.append(arguments['id_column_number'])
                for number in arguments['column_numbers']:
                    column_numbers.append(number)
                data = pd.read_csv(src_file, delimiter=delimiter, header=None, usecols=column_numbers)
                ids = data[[column_numbers[0]]].values.tolist()
                del data[column_numbers[0]]
        elif extension == '.shp':
            ids = []
            data = []
            with fiona.open(src_file) as src:
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
    r = {
        "cluster_centers": json.dumps(centers),
        "ids": ids,
        "labels": json.dumps(kmeans.labels_.tolist()),
    };

    response = make_response(r, 200);
    response.headers['content-type'] = 'application/json; charset=utf-8';
    return response;

@app.route("/redirect")
def redirect_to_get():
    location = url_for("get");
    current_app.logger.info("Redirecting to %s", location)
    return redirect(location);

@app.route("/unauthorized")
def unauthorized():
    current_app.logger.info("Not authorized");
    abort(401)

@app.route("/fail")
def fail():
    h = request.headers;
    p = request.values;
    raise Exception("ooops");
