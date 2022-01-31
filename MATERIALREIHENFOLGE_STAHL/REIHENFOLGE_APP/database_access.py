import pandas as pd
import pyodbc
# test MS Access Drivers availability for Python
# msa_drivers = [x for x in pyodbc.drivers() if 'ACCESS' in x.upper()]
# print(f'MS-Access Drivers : {msa_drivers}')
# make sure, that "Microsoft Access Driver (*.mdb, *.accdb)" is part of the drivers

def get_coils_from_access_db():

    """
    This function is used to get the databse
    :return: List of two panda dataframes, one for coils and one for dummy coils
    """

    # Checking Database Connection in MS Access
    # insert correct path
    try:
        con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=.\Coils_Test.accdb;'
        conn = pyodbc.connect(con_string)
        print("Connected To Database")

    except pyodbc.Error as e:
        print("Error in Connection", e)

    # Selecting Data from MS Access Database
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Coils_default')
            coils = pd.DataFrame(cursor.fetchall())
            get_columns = [column[0] for column in cursor.description]
            # TODO: add column names
            # coils.columns = get_columns
            coils.head()
            # load dummy coils:
            cursor.execute('SELECT * FROM dummy_coils')
            dummy_coils = pd.DataFrame(cursor.fetchall())
            get_dummy_columns = [column[0] for column in cursor.description]
            # TODO: add column names
            # dummy_coils.columns = get_dummy_columns
            dummy_coils.head()

        except pyodbc.Error as e:
            print("Error in Connection")

#TODO: add dummy_coils
 #   dummy_coils = pd.read_excel("./default_database_dummy_coils.xlsx")

    return [coils, dummy_coils]