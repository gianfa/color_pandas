""" Styles

    Ready-to-use styles.

"""

from enum import Enum

class Highlighter(str, Enum):
    YELLOW = 'background-color: rgb(245, 197, 66); color:black'
    RED = 'background-color: rgb(230, 24, 21); color: black'
    BLACK = 'background-color: black; color: white'

