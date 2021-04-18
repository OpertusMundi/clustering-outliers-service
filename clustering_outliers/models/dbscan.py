from sklearn.cluster import DBSCAN

from ..forms import BaseDBScanForm
from .utils import get_dataframe


def dbscan(form: BaseDBScanForm, file_path: str) -> dict:

    features, ids = get_dataframe(form, file_path)

    epsilon = form.epsilon.data if form.epsilon.data else 0.5

    min_samples = form.min_samples.data if form.min_samples.data else 5

    model = DBSCAN(eps=epsilon, min_samples=min_samples)

    model.fit(features)

    core_sample_indices = model.core_sample_indices_.tolist()

    components = model.components_.tolist()

    labels = model.labels_.tolist()

    response = {
        "core_sample_indices": core_sample_indices,
        "components": components,
        "ids": ids,
        "labels": labels,
    }

    return response
