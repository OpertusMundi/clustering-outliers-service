from sklearn.cluster import KMeans

from .utils import get_dataframe, get_kmeans_k
from ..forms import BaseKMeansForm


def kmeams(form: BaseKMeansForm, file_path: str) -> dict:

    features, ids = get_dataframe(form, file_path)

    k = form.k.data if form.k.data else get_kmeans_k(features)

    # Initilize and run kMeans clustering
    kmeans = KMeans(
        init="random",
        n_clusters=k,
        n_init=10,
        max_iter=300,
        random_state=42
    )

    kmeans.fit(features)

    # The results are the cluster centers and element membership
    centers = [center.tolist() for center in kmeans.cluster_centers_]

    response = {
        "cluster_centers": centers,
        "ids": ids,
        "labels": kmeans.labels_.tolist(),
    }

    return response
