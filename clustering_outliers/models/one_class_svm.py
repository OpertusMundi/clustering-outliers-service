from sklearn.svm import OneClassSVM

from .utils import get_dataframe
from ..forms import BaseOCSVMForm


def one_class_svm(form: BaseOCSVMForm, file_path: str) -> dict:

    features, ids = get_dataframe(form, file_path)

    degree = form.degree.data if form.degree.data else 3

    model = OneClassSVM(degree=degree)

    pred = model.fit_predict(features)

    outliers = {ids[i][0]: features.tolist()[i] for i, x in enumerate(pred) if x == -1}

    return outliers
