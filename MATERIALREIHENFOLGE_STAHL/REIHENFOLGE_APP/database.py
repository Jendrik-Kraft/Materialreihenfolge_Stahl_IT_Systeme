import pandas as pd
import pyodbc
import numpy as np

# test MS Access Drivers availability for Python
# msa_drivers = [x for x in pyodbc.drivers() if 'ACCESS' in x.upper()]
# print(f'MS-Access Drivers : {msa_drivers}')
# make sure, that "Microsoft Access Driver (*.mdb, *.accdb)" is part of the drivers

def get_coils_from_database():
    """
    This function is used to get the databse from MS Access
    :return: List of two panda dataframes, one for coils and one for dummy coils
    """

    # Establish Database Connection in MS Access
    # CoilsDatabase includes default data and dummy coils
    try:
        con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=REIHENFOLGE_APP\CoilsDatabase.accdb;'
        conn = pyodbc.connect(con_string)
        print("Connected To Database")

    except pyodbc.Error as e:
        print("Error in Connection", e)

    # Selecting Data from MS Access Database
    try:
        cursor = conn.cursor()

        # load default data:
        cursor.execute('SELECT * FROM Coils_default')       # "Coils_default" is the table with the default data
        coils_list = cursor.fetchall()                      # data is pulled as list
        coils_array = np.array(coils_list)                  # convert list to array
        get_columns = [column[0] for column in cursor.description]  # collects columnnames
        # now the array can be nicely written into DataFrame including the columnnames
        coils = pd.DataFrame(data=coils_array, columns=get_columns)
        #print(coils.head())

        # load dummy coils:
        cursor.execute('SELECT * FROM dummy_coils')         # "dummy_coils" is the table with the dummy coil data
        dummy_coils_list = cursor.fetchall()                # data is pulled as list
        dummy_coils_array = np.array(dummy_coils_list)      # convert list to array
        get_dummy_columns = [column[0] for column in cursor.description] # collects columnnames
        dummy_coils = pd.DataFrame(data=dummy_coils_array, columns=get_dummy_columns)   # array to DataFrame
        # print(dummy_coils.head())

    except pyodbc.Error as e:
        print("Error in Connection")
        coils = None
        dummy_coils = None

    return [coils, dummy_coils]