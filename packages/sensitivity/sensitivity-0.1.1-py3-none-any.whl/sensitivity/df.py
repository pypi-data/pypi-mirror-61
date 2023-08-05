from typing import Dict, Any, Callable, Sequence, Optional
import itertools
from copy import deepcopy
import pandas as pd
import pd_utils
from pandas.io.formats.style import Styler

from sensitivity.colors import _get_color_map


def sensitivity_df(sensitivity_values: Dict[str, Any], func: Callable,
                   result_name: str = 'Result', **func_kwargs) -> pd.DataFrame:
    """
    Creates a DataFrame containing the results of sensitivity analysis.

    Runs func with the cartesian product of the possible values for each argument, passed
    in sensitivity_values.

    :param sensitivity_values: Dictionary where keys are func's argument names and values are lists of possible
        values to use for that argument.
    :param func: Function that accepts arguments with names matching the keys of sensitivity_values, and outputs a
        scalar value.
    :param result_name: Name for result shown in graph color bar label
    :param func_kwargs: Additional arguments to pass to func, regardless of the sensitivity values picked
    :return: a DataFrame containing the results from sensitivity analysis on func
    """
    sensitivity_cols = list(sensitivity_values.keys())
    df = pd.DataFrame(columns=sensitivity_cols + [result_name])
    for i in itertools.product(*sensitivity_values.values()):
        base_param_dict = dict(zip(sensitivity_cols, i))
        param_dict = deepcopy(base_param_dict)
        param_dict.update(func_kwargs)
        result = func(**param_dict)
        base_param_dict.update({result_name: result})
        df = df.append(pd.DataFrame(pd.Series(base_param_dict)).T)
    df.reset_index(drop=True, inplace=True)
    df = df.convert_dtypes()

    return df


def _two_variable_sensitivity_display_df(df: pd.DataFrame, col1: str, col2: str,
                                         result_col: str = 'Result') -> pd.DataFrame:
    selected_df = df[[col1, col2, result_col]]
    wide_df = pd_utils.long_to_wide(
        selected_df,
        col1,
        result_col,
        colindex=col2,
        colindex_only=True
    ).set_index(col1)

    return wide_df


def _style_sensitivity_df(df: pd.DataFrame, col1: str, col2: Optional[str] = None, result_col: str = 'Result',
                          reverse_colors: bool = False,
                          col_subset: Optional[Sequence[str]] = None) -> Styler:
    if col2 is not None:
        caption = f'{result_col} - {col1} vs. {col2}'
    else:
        caption = f'{result_col} vs. {col1}'

    color_str = _get_color_map(reverse_colors=reverse_colors)
    return df.style.background_gradient(
        cmap=color_str, subset=col_subset, axis=None
    ).set_caption(caption)

