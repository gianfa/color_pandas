#!/usr/bin/env python3
"""

"""
import types
import pandas as pd

#from pandas.io.formats.style import Styler

# base #

def get_df_or_styler(df):
    df_ = None
    if type(df) == pd.DataFrame: df_ = df.style
    elif type(df) == pd.io.formats.style.Styler: df_ = df
    assert not df_ is None
    return df_

def df_st_on_single_cell_of_s(ss, id, col, css):
    default = ''

    if ss.name == col:
        ss_ = ss.copy()
        ss_.loc[id] = css
        ss_[~ss_.index.isin([id])] = default
        return ss_
    return [default for _ in ss.values]

def df_st_on_single_cell(df:pd.DataFrame, id, col:str, css:str):
    """
        Return (pandas.io.formats.style.Styler)

        Example:
            css = 'background-color: rgb(128, 203, 2)'
            df_s = style_on_single_cell(df[:5], 3, 'sepal_length', css)
    """
    assert type(df) == pd.DataFrame
    assert type(id) == int, "`id` must be int"
    df_ = get_df_or_styler(df)
    # to named col #
    partial = lambda ss: df_st_on_single_cell_of_s(ss, id, col, css)
    return df_.apply(partial)

def df_st_conditional_on_s(
    ss:pd.Series,
    condition:types.LambdaType or types.FunctionType,
    col:str,
    css_true:str,
    css_default:str=''):
    """
        Example:
            >>> df = sns.load_dataset('iris')
            >>> condition = lambda x: x>5
            >>> col = 'sepal_length'
            >>> css_true = 'background-color: rgb(128, 203, 2)'
            >>> css_default = ''
            >>> partial = lambda ss:df_st_conditional_on_s(ss, condition, col, css_true, css_default)
            >>> return df.style.apply(partial)
    """
    if ss.name == col:
        ss_ = ss.copy()
        idxs = ss[condition(ss)].index; print(ss.name, idxs)
        ss_.loc[idxs] = css_true
        ss_[~ss_.index.isin(idxs)] = css_default
        return ss_
    return [css_default for _ in ss.values]

def df_st_conditional(
    df:pd.DataFrame,
    condition,
    col:str,
    css_true:str,
    css_default:str=''
):
    """Conditionally apply css on a DF column

    Args:
        df (pd.DataFrame): The original DF
        condition ([type]): The condition according to which to apply the style
        col (str): Name of the column to modify
        css_true (str): The css to apply when the condition is verified
        css_default (str, optional): The css to apply when the condition is not verified. Defaults to ''.

    Returns:
        ():

    Example:
        >>> df = sns.load_dataset('iris')
        >>> condition = lambda x: x>5
        >>> df_st_conditional(df[:5], lambda x: x>5, 'sepal_length', css)
    """
    assert type(col) == str, f"`col` must be str, instead it was {type(col)}"
    assert type(condition) == types.FunctionType, f"`condition` must be a Function, instead it was type(condition)"
    partial = lambda ss:df_st_conditional_on_s(ss, condition, col, css_true, css_default)
    return df.style.apply(partial)

#### Experimental Functions ####

def red_if_ratio_gt(x, ratio=0.5, suff ='_samp'):
    vals = []
    for k,v in x.items():
        ends_with_suff = suff in k[-len(suff):]
        #ends_not_with_suff = not ends_with_suff
        #exists_suff = f"{k}{suff}" in x.keys()
        #is_bulk_col = exists_suff and ends_not_with_suff
        is_not_bulk_col = ends_with_suff
        vals.append("")
        if is_not_bulk_col:
            col_bulk = k[:-len(suff)]
            try:
                ratio_ = abs(x[k]-x[col_bulk])/max(x[k],x[col_bulk])
                if ratio_ > ratio:
                    vals[-1] = "background: cyan"
            except:
                None
    return vals

#### Functions to review ####
# The following come from experiments,
#   actually there are pandas functions which
#   already do what these do.
#   See below
#      https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.io.formats.style.Styler.highlight_null.html

def df_st_piece_highlight_ALL_NULLS(s):
    """
    Highlights the row if any of the columns respect the condition here defined
    """
    row = pd.Series(data=False, index=s.index)
    condition = lambda s: s.loc['density'] == 0
    return ['background-color: rgb(255, 204, 204)' if condition(s) else '' for v in row]

def df_st_piece_highlight_ALL_DENSE(s):
    """
    Highlights the row if any of the columns respect the condition here defined
    """
    row = pd.Series(data=False, index=s.index)
    condition = lambda s: s.loc['density'] == 1
    return ['background-color: rgb(128, 203, 2)' if condition(s) else '' for v in row]

    
    
def df_style_apply_col_gradient(df, columns):
    df_ = get_df_or_styler(df)
    return df_.background_gradient(axis=0,
            cmap='YlOrRd', subset=columns
        )

def df_style_apply_row_highlight_ALL_NULLS(df, columns):
    df_ = get_df_or_styler(df)
    return df_.apply(df_st_piece_highlight_ALL_NULLS, axis=1)

def df_style_apply_row_highlight_ALL_DENSE(df, columns):
    df_ = get_df_or_styler(df)
    return df_.apply(df_st_piece_highlight_ALL_DENSE, axis=1)


