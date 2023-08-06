from statsmodels import api as sm
from typing import List, Union

from regtools.fe.dataprep import fixed_effects_reg_df_and_cols_dict
from regtools.fe.tools import extract_all_dummy_cols_from_dummy_cols_dict
from regtools.interact import create_interaction_variables, _collect_variables_from_interaction_tuples
from regtools.lag.main import create_lagged_variables_return_yvars_xvars_interaction_tuples
from regtools.tools import _to_list_if_str, _to_list_if_tuple
from regtools.cluster import estimate_model_handling_cluster


def _create_reg_df_y_x_and_dummies(df, yvar, xvars, cluster=False, cons=True, fe=None, interaction_tuples=None,
                                   num_lags=0, lag_variables='xvars', lag_period_var='Date', lag_id_var='TICKER',
                                   fill_method='ffill', fill_limit: int = None):
    # Handle lags
    df, reg_yvar, reg_xvars, interaction_tuples, lag_variables = create_lagged_variables_return_yvars_xvars_interaction_tuples(
        df, yvar, xvars,
        interaction_tuples=interaction_tuples,
        num_lags=num_lags,
        lag_variables=lag_variables,
        lag_period_var=lag_period_var,
        lag_id_var=lag_id_var,
        fill_method=fill_method,
        fill_limit=fill_limit
    )

    fe = _set_fe(fe)
    interaction_tuples = _set_interaction_tuples(interaction_tuples)
    cluster = _set_cluster(cluster)
    regdf, y, X, dummy_cols_dict = _get_reg_df_y_x(df, reg_yvar, reg_xvars, cluster, cons, fe, interaction_tuples)
    return regdf, y, X, dummy_cols_dict, lag_variables


def _post_reg_cleanup(df, num_lags, lag_variables):
    # Cleanup lags
    if num_lags != 0:
        df.drop(lag_variables, axis=1, inplace=True)


def _estimate_handling_robust_and_cluster(regdf, model, robust, cluster, **fit_kwargs):
    assert not (robust and cluster)  # need to pick one of robust or cluster

    if robust:
        return model.fit(cov_type='HC1', **fit_kwargs)

    if cluster:
        return estimate_model_handling_cluster(
            regdf,
            model,
            cluster,
            **fit_kwargs
        )

    return model.fit(**fit_kwargs)


def _get_reg_df_y_x(df, yvar, xvars, cluster, cons, fe, interaction_tuples):
    all_xvars = _collect_all_variables_from_xvars_and_interaction_tuples(xvars, interaction_tuples)
    regdf = _drop_missings_df(df, yvar, all_xvars, cluster, fe)
    y, X, dummy_cols_dict = _y_X_from_df(regdf, yvar, xvars, cons, fe, interaction_tuples)

    return regdf, y, X, dummy_cols_dict


def _drop_missings_df(df, yvar, xvars, cluster, fe):
    drop_set = [yvar] + xvars
    if cluster:
        drop_set += cluster
    if fe is not None:
        drop_set += fe

    return df.dropna(subset=drop_set)


def _y_X_from_df(regdf, yvar, xvars, cons, fe, interaction_tuples):

    if fe is not None:
        regdf, dummy_cols_dict = fixed_effects_reg_df_and_cols_dict(regdf, fe)
        model_xvars = xvars + extract_all_dummy_cols_from_dummy_cols_dict(dummy_cols_dict)
    else:
        dummy_cols_dict = None
        model_xvars = xvars.copy()

    if interaction_tuples:
        interaction_vars = create_interaction_variables(regdf, interaction_tuples)
        model_xvars += interaction_vars

    y = regdf[yvar]
    X = regdf.loc[:, model_xvars]

    if cons:
        X = sm.add_constant(X)

    return y, X, dummy_cols_dict


def _set_fe(fe):
    if fe is None:
        return None
    else:
        return _to_list_if_str(fe)


def _set_interaction_tuples(interaction_tuples):
    if interaction_tuples is None:
        return []
    else:
        return _to_list_if_tuple(interaction_tuples)


def _set_cluster(cluster: Union[bool, List[str]]) -> List[str]:
    if cluster is False:
        return []
    else:
        return _to_list_if_str(cluster)


def _collect_all_variables_from_xvars_and_interaction_tuples(xvars, interaction_tuples):
    interaction_vars = _collect_variables_from_interaction_tuples(interaction_tuples)
    return list(set(xvars + interaction_vars))


def _is_normal_reg_str(reg_str):
    return reg_str in ('reg', 'normal', 'ols') or reg_str == None