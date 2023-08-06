from linearmodels import FamaMacBeth, PanelOLS

def get_model_class_by_string(model_string):
    if _is_ols_str(model_string):
        return PanelOLS
    elif _is_fama_macbeth_str(model_string):
        return FamaMacBeth
    else:
        raise ValueError(f'model string does not signify ols, probit, logit, or fama macbeth. got {model_string}')

def _is_fama_macbeth_str(model_string: str) -> bool:
    simple_str = model_string.lower().strip().replace('-','').replace('_','').replace(' ','')
    return simple_str in ('famamacbeth', 'fmb', 'fb', 'fm', 'fmacbeth','famam','fmbreg','fmreg')

# Note: add model str functions here as they are created. This will feed into _is_linearmodels_str
model_str_funcs = [
    _is_fama_macbeth_str
]

def _is_linearmodels_str(model_string: str) -> bool:
    return any([is_model_str_func(model_string) for is_model_str_func in model_str_funcs])

def _is_ols_str(model_string):
    return model_string.lower().strip() in (
        'ols','o','reg','least squares', 'ordinary least squares', 'panel', 'panel ols', 'panelols'
    )