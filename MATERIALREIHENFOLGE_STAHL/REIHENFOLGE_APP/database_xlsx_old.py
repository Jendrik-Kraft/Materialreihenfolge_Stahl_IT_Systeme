import pandas as pd


def get_coils_from_database_old():
    """
    This function was used to get the databse from Excel
    :return: List of two panda dataframes, one for coils and one for dummy coils
    """
    dummy_coils = pd.read_excel("./default_database_dummy_coils.xlsx")
    # print(dummy_coils.head())
    coils = pd.read_excel("./default_database1.xlsx")
    # print(coils.head())
    return [coils, dummy_coils]
