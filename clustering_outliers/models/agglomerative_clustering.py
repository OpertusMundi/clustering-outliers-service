from sklearn.cluster import AgglomerativeClustering

from ..forms import BaseAgglomerativeForm
from .utils import get_dataframe


def agglomerative_clustering(form: BaseAgglomerativeForm, file_path: str) -> dict:

    features, ids = get_dataframe(form, file_path)

    n_clusters = form.k.data if form.k.data else 2

    linkage = form.linkage.data if form.linkage.data else 'ward'

    distance_threshold = form.dist_threshold if form.dist_threshold.data else None

    model = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage, distance_threshold=distance_threshold)

    model.fit(features)

    n_clusters = model.n_clusters_

    n_leaves = model.n_leaves_

    n_connected_components = model.n_connected_components_

    children = model.children_.tolist()

    labels = model.labels_.tolist()

    response = {
        "n_clusters": n_clusters,
        "n_leaves": n_leaves,
        "n_connected_components": n_connected_components,
        "children": children,
        "ids": ids,
        "labels": labels,
    }

    return response
