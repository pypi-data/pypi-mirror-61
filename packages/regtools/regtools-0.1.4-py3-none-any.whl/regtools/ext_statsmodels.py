import numpy as np
import pandas as pd

from scipy import stats

from statsmodels.iolib.summary2 import summary_params
from statsmodels.iolib.table import SimpleTable
from statsmodels.iolib.tableformatting import fmt_params

from statsmodels.iolib.summary2 import (
    lrange,
    lzip,
    reduce,
    _col_params,
    _make_unique,
    _col_info,
    Summary,
)


def summary_col(
    results,
    float_format="%.4f",
    model_names=[],
    stars=False,
    info_dict=None,
    regressor_order=[],
):
    """
    Summarize multiple results instances side-by-side (coefs and SEs)

    Parameters
    ----------
    results : statsmodels results instance or list of result instances
    float_format : string
        float format for coefficients and standard errors
        Default : '%.4f'
    model_names : list of strings of length len(results) if the names are not
        unique, a roman number will be appended to all model names
    stars : bool
        print significance stars
    info_dict : dict
        dict of lambda functions to be applied to results instances to retrieve
        model info. To use specific information for different models, add a
        (nested) info_dict with model name as the key.
        Example: `info_dict = {"N":..., "R2": ..., "OLS":{"R2":...}}` would
        only show `R2` for OLS regression models, but additionally `N` for
        all other results.
        Default : None (use the info_dict specified in
        result.default_model_infos, if this property exists)
    regressor_order : list of strings
        list of names of the regressors in the desired order. All regressors
        not specified will be appended to the end of the list.
    """

    # TODO [#1]: replace summary_col with an import from statsmodels
    #
    # the purpose of recreating the summary_col function is becuase of issue
    # #3767 in statsmodels:
    # https://github.com/statsmodels/statsmodels/issues/3767
    # Which can cause coefficients to become mismatched when using regressor_order.
    # I have patched the issue by replacing np.unique with pd.unique.

    if not isinstance(results, list):
        results = [results]

    cols = [_col_params(x, stars=stars, float_format=float_format) for x in results]

    # Unique column names (pandas has problems merging otherwise)
    if model_names:
        colnames = _make_unique(model_names)
    else:
        colnames = _make_unique([x.columns[0] for x in cols])
    for i in range(len(cols)):
        cols[i].columns = [colnames[i]]

    merg = lambda x, y: x.merge(y, how="outer", right_index=True, left_index=True)
    summ = reduce(merg, cols)

    if regressor_order:
        varnames = summ.index.get_level_values(0).tolist()
        ordered = [x for x in regressor_order if x in varnames]
        unordered = [x for x in varnames if x not in regressor_order + [""]]
        order = ordered + list(np.unique(unordered))

        f = lambda idx: sum([[x + "coef", x + "stde"] for x in idx], [])
        summ.index = f(pd.unique(varnames))
        summ = summ.reindex(f(order))
        summ.index = [x[:-4] for x in summ.index]

    idx = pd.Series(lrange(summ.shape[0])) % 2 == 1
    summ.index = np.where(idx, "", summ.index.get_level_values(0))

    # add infos about the models.
    if info_dict:
        cols = [
            _col_info(x, info_dict.get(x.model.__class__.__name__, info_dict))
            for x in results
        ]
    else:
        cols = [_col_info(x, getattr(x, "default_model_infos", None)) for x in results]
    # use unique column names, otherwise the merge will not succeed
    for df, name in zip(cols, _make_unique([df.columns[0] for df in cols])):
        df.columns = [name]
    merg = lambda x, y: x.merge(y, how="outer", right_index=True, left_index=True)
    info = reduce(merg, cols)
    dat = pd.DataFrame(np.vstack([summ, info]))  # pd.concat better, but error
    dat.columns = summ.columns
    dat.index = pd.Index(summ.index.tolist() + info.index.tolist())
    summ = dat

    summ = summ.fillna("")

    smry = Summary()
    smry.add_df(summ, header=True, align="l")
    smry.add_text("Standard errors in parentheses.")
    if stars:
        smry.add_text("* p<.1, ** p<.05, ***p<.01")

    return smry


def update_statsmodel_result_with_new_cov_matrix(result, cov_matrix: pd.DataFrame):
    """
    Note: inplace

    Statsmodels results have caching going on. Need to update all the properties
    which depend on the covariance matrix

    """

    result.cov_params = lambda: cov_matrix
    result.bse = pd.Series(
        np.sqrt(np.diag(result.cov_params())), index=result.model.exog_names
    )
    result.tvalues = result.params / result.bse

    if result.use_t:
        df_resid = getattr(result, "df_resid_inference", result.df_resid)
        result.pvalues = stats.t.sf(np.abs(result.tvalues), df_resid) * 2
    else:
        result.pvalues = stats.norm.sf(np.abs(result.tvalues)) * 2

    _update_statsmodel_result_summary_after_cov_matrix_changed(result)


def _update_statsmodel_result_summary_after_cov_matrix_changed(result):
    """
    Note: inplace
    """
    # Create new param/stderr section of summary
    new_param_stderr = summary_params(result)
    new_table = SimpleTable(
        new_param_stderr.values,
        headers=list(new_param_stderr.columns),
        stubs=list(new_param_stderr.index),
        txt_fmt=fmt_params,
    )

    # Create summary object with param/stderr table replaced
    summ = result.summary()
    summ.tables[1] = new_table

    # Assign summary method of result to return this summary object
    result.summary = lambda: summ

    # Repeat steps for summary2, which only requires df and not SimpleTable
    summ2 = result.summary2()
    summ2.tables[1] = new_param_stderr
    result.summary2 = lambda: summ2
