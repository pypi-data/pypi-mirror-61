"""
typelike.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

import numpy as np
import pandas as pd

__all__ = [
    'typelike'
]


# A list of types
dtypes = {
    'int': int,
    'float': float,
    'str': str,
    'list': list,
    'tuple': tuple,
    'set': set,
    'dict': dict,
    'numpy': np.ndarray,
    'series': pd.Series,
    'dataframe': pd.DataFrame
}


def typelike(anything):
    """
    Get the type of anything

    Applies some logic to parse anything

    Parameters
    ----------
    anything : Anything

    Returns
    -------
    object
        Type of `anything`
    """

    # By default, set the type to the type of anything
    dtype = type(anything)

    # If anything is a string, try to parse
    if isinstance(anything, str):
        dtype = dtypes.get(anything.lower(), dtype)

    # Return
    return dtype
