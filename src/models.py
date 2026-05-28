from darts.models import NaiveSeasonal, LinearRegressionModel


def train_naive_seasonal(train_series, seasonality: int = 7):
    model = NaiveSeasonal(K=seasonality)
    model.fit(train_series)
    return model


def train_linear_regression(train_series, lags: int = 30):
    model = LinearRegressionModel(lags=lags)
    model.fit(train_series)
    return model