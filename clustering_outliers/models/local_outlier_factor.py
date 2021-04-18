from sklearn.neighbors import LocalOutlierFactor

from ..forms import BaseLOFForm
from .utils import get_dataframe


def local_outlier_factor(form: BaseLOFForm, file_path: str) -> dict:

    features, ids = get_dataframe(form, file_path)

    n_neighbors = form.n_neighbors.data if form.n_neighbors.data else 20

    model = LocalOutlierFactor(n_neighbors=n_neighbors)

    pred = model.fit_predict(features)

    outliers = {ids[i][0]: features.tolist()[i] for i, x in enumerate(pred) if x == -1}

    return outliers
