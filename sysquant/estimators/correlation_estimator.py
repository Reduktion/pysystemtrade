import pandas as pd

from sysquant.estimators.correlations import correlationEstimate, create_boring_corr_matrix
from sysquant.estimators.exponential_correlation import exponentialCorrelation
from sysquant.fitting_dates import fitDates
from sysquant.estimators.generic_estimator import genericEstimator

class correlationEstimator(genericEstimator):
    def __init__(
        self,
        data_for_correlation: pd.DataFrame,
        using_exponent: bool = True,
        **kwargs
    ):
        super().__init__(data_for_correlation,
                         using_exponent=using_exponent,
                         **kwargs)



    def calculate_estimate_normally(self, fit_period: fitDates) -> correlationEstimate:
        data_for_correlation = self.data
        kwargs_for_estimator = self.kwargs_for_estimator
        corr_matrix = correlation_estimator_for_subperiod(data_for_correlation=data_for_correlation,
                                                          fit_period=fit_period,
                                                          **kwargs_for_estimator)

        return corr_matrix


    def calculate_exponential_estimator_for_entire_dataset(self) -> exponentialCorrelation:
        kwargs_for_estimator = self.kwargs_for_estimator
        exponential_correlation = \
            exponentialCorrelation(self.data, **kwargs_for_estimator)

        return exponential_correlation

    def estimate_if_no_data(self) -> correlationEstimate:
        columns = self.data.columns
        size = len(columns)

        return create_boring_corr_matrix(size)


def correlation_estimator_for_subperiod(data_for_correlation,
                                                     fit_period: fitDates,
                          cleaning: bool = True,
                          floor_at_zero: bool = True,
                          **_ignored_kwargs):

    subperiod_data = data_for_correlation[fit_period.fit_start: fit_period.fit_end]

    corr_matrix_values = subperiod_data.corr()
    corr_matrix = correlationEstimate(corr_matrix_values, data_for_correlation.columns)
    if cleaning:
        corr_matrix = corr_matrix.clean_corr_matrix_given_data(data_for_correlation=data_for_correlation,
                                                               fit_period=fit_period)

    if floor_at_zero:
        corr_matrix = corr_matrix.floor_correlation_matrix(floor = 0.0)

    return corr_matrix