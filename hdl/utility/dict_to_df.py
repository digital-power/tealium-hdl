import pandas as pd

def dict_to_df(datalayer, filename):
    """Conver datalayer Dictionary into Pandas dataframe"""
    datalayer_df = pd.DataFrame([datalayer.keys(), datalayer.values()]).transpose()
    datalayer_df.columns = ['Variable', filename]

    return datalayer_df
