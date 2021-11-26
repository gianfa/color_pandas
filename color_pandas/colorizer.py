"""

"""
# import sys
# sys.path.append('../')
from functools import wraps

from .funx import *
from .styles import  Highlighter


@pd.api.extensions.register_dataframe_accessor("colorizer")
class ColorPandas:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj
        self.history=[]
        self.styles=[]
        self._highlighter_default = Highlighter.YELLOW

    def add_to_history(func):
        # ref: https://stackoverflow.com/questions/52992049/command-history-for-class-instances
        @wraps(func)
        def wrapper(self, *args, **kw):
            self.history.append(func.__name__)
            return func(self, *args, **kw)
        return wrapper

    @add_to_history
    def style_at(self, col, id, css):
        return df_st_on_single_cell(self._obj, id, col, css)

    @add_to_history
    def style_if(
        self,
        col:str,
        condition:types.LambdaType or types.FunctionType,
        css_true:str,
        css_default:str=''
    ):
        assert type(col) == str, f"`col` must be str, instead it was {type(col)}"
        assert type(condition) == types.FunctionType, f"`condition` must be a Function, instead it was type(condition)"
        return df_st_conditional(self._obj, condition, col, css_true, css_default)

    @add_to_history
    def highlight_at(
        self,
        col:str,
        id:int,
        css:str=None,
    ):
        """ Highlights a single cell

        Args:
            id (int): The index of the cell
            col (str): The name of the column of the cell
            css (str, optional): A css line to customize the highlightningss. Defaults to None.

        Returns:
            (pandas.io.formats.style.Styler):
                The style object containing the DF with the cell highlighted

        Examples:
            >>> from color_pandas.colorizer import ColorPandas
            >>> import seaborn as sns # only for dataset loading
            >>> df = sns.load_dataset('iris')
            >>> df[:5].colorizer.highlight_at('sepal_length', 4)
        """
        assert type(col) == str
        assert type(id) == int
        if css is None:
            css = self._highlighter_default
        return self.style_at(col, id, css)

    @add_to_history
    def highlight_if(
        self,
        col:str,
        condition:types.LambdaType or types.FunctionType,
        css_true:str=None,
        css_default:str=''
    ):
        if css_true is None:
            css_true = self._highlighter_default
        return self.style_if(col, condition, css_true, css_default)
