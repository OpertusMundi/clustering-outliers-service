from sklearn.ensemble import IsolationForest

from ..forms import BaseIsoForestForm
from .utils import get_dataframe


def isolation_forest(form: BaseIsoForestForm, file_path: str) -> dict:

    features, ids = get_dataframe(form, file_path)

    n_estimators = form.n_estimators.data if form.n_estimators.data else 100

    max_samples = form.max_samples.data if form.max_samples.data else 'auto'

    model = IsolationForest(n_estimators=n_estimators, max_samples=max_samples)

    pred = model.fit_predict(features)

    outliers = {ids[i][0]: features.tolist()[i] for i, x in enumerate(pred) if x == -1}

    return outliers
