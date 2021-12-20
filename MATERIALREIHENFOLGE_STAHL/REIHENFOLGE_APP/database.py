import pandas as pd


def get_coils_from_database():
    """
    This function is used to get the databse
    :return: List of two panda dataframes, one for coils and one for dummy coils
    """
    dummy_coils = pd.read_excel("./REIHENFOLGE_APP/default_database_dummy_coils.xlsx")
    coils = pd.read_excel("./REIHENFOLGE_APP/default_database1.xlsx")
    return [coils, dummy_coils]
