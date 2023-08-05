#!/usr/bin/env python


import os

import numpy as np
import pandas as pd
from .conftest import file_exists, file_exists_and_not_empty


def test_rpm_normalization(various_analysis):
    for analysis in [a for a in various_analysis if a.data_type == "RNA-seq"]:
        qnorm = analysis.normalize_rpm(save=False)
        assert qnorm.dtypes.all() == np.float
        assert hasattr(analysis, "matrix_norm")
        rpm_file = os.path.join(
            analysis.results_dir, analysis.name + ".matrix_norm.csv"
        )
        assert not file_exists(rpm_file)
        qnorm = analysis.normalize_rpm(save=True)
        assert file_exists_and_not_empty(rpm_file)
        assert hasattr(analysis, "matrix_norm")


def test_normalize(rnaseq_analysis):
    qnorm = rnaseq_analysis.normalize_rpm(save=False)
    assert isinstance(qnorm, pd.DataFrame)
    assert hasattr(rnaseq_analysis, "matrix_norm")
    del rnaseq_analysis.matrix_norm

    qnorm_d = rnaseq_analysis.normalize(method="rpm", save=False)
    assert isinstance(qnorm_d, pd.DataFrame)
    assert hasattr(rnaseq_analysis, "matrix_norm")
    assert np.array_equal(qnorm_d, qnorm)
    del rnaseq_analysis.matrix_norm

    qnorm = rnaseq_analysis.normalize_quantiles(save=False)
    assert hasattr(rnaseq_analysis, "matrix_norm")
    del rnaseq_analysis.matrix_norm

    qnorm_d = rnaseq_analysis.normalize(method="quantile", save=False)
    assert isinstance(qnorm_d, pd.DataFrame)
    assert hasattr(rnaseq_analysis, "matrix_norm")
    assert np.array_equal(qnorm_d, qnorm)
    del rnaseq_analysis.matrix_norm


def test_annotate_features(rnaseq_analysis):
    rnaseq_analysis.get_matrix_stats(matrix="matrix_raw")
    rnaseq_analysis.annotate_features(matrix="matrix_raw")
    f = os.path.join(
        rnaseq_analysis.results_dir, rnaseq_analysis.name + ".matrix_features.csv"
    )
    assert hasattr(rnaseq_analysis, "matrix_features")
    assert file_exists_and_not_empty(f)

    cols = [
        "mean",
        "variance",
        "std_deviation",
        "dispersion",
        "qv2",
        "amplitude",
        "iqr",
    ]  # from stats

    assert all([c in rnaseq_analysis.matrix_features.columns.tolist() for c in cols])


def test_plot_expression_characteristics(various_analysis):
    for analysis in [a for a in various_analysis if a.data_type == "RNA-seq"]:
        analysis.normalize()
        analysis.plot_expression_characteristics()
        assert file_exists(os.path.join(analysis.results_dir, "quality_control"))
