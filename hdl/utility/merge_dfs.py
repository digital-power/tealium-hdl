import pandas as pd
from functools import reduce

def merge_dfs(dataframe_list):
    """Merge several datalayer dataframes on the Variable Column"""
    merged_dfs = reduce(lambda x, y: pd.merge(
        left=x,
        right=y,
        on='Variable',
        how='outer'), dataframe_list).fillna('')

    return merged_dfs
