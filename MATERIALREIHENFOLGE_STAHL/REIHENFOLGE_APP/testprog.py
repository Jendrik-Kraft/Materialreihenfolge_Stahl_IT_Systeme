import pandas as pd
import json
from django.shortcuts import render
# Create your views here.
import random
#from database import *
from utility import *
import pyodbc
import numpy as np

def find_fusible_coils(coils, tolerance_h_per, tolerance_w_abs):
    """
    This functions finds each coil pair from coils if both, height and width, are in given tolerance
    :param coils: Panda Dataframe of coils with position number, width and height
    :param tolerance_h_per: Height tolerance in percent
    :param tolerance_w_abs: Absolute width tolerance
    :return: List of lists for each fitting pair, e.g. [[1, 5], [2, 4], [2, 5]]
    """
    # TODO Clarification needed: What happens if coil1*(1+tolerance) does not include coil2, but coil2*(1-tolerance)
    #  does include coil1? (e.g. 10%, coil1=100 coil2=111 100+10%=110, 111-10%=99.9)
    # Calculate top and bottom tolerance for height given in percent
    tolerance_h_top = 1+tolerance_h_per/100
    tolerance_h_bottom = 1-tolerance_h_per/100
    fusible_coils_temp = []
    coils_list = coils.values.tolist()
    for coil in coils_list:
        for coil_compare in coils_list:
            # Do not use same coil for comparison
            if coil[0] == coil_compare[0]:
                pass
            # Check if the coil is in both tolerances
            elif (tolerance_h_top * coil[1] >= coil_compare[1] >= tolerance_h_bottom * coil[1]) and (
                     coil[2] + tolerance_w_abs >= coil_compare[2] >= coil[2]-tolerance_w_abs):

                # Append coil to the list with lower coil value first - to delete duplicate entry e.g. [1 5] and [5 1]
                if coil[0] < coil_compare[0]:
                    fusible_coils_temp.append([coil[0], coil_compare[0]])
                else:
                    fusible_coils_temp.append([coil_compare[0], coil[0]])

    fusible_coils = []
    # Delete duplicate entries
    for elem in fusible_coils_temp:
        if elem not in fusible_coils:
            fusible_coils.append(elem)

    return fusible_coils

def get_coils_from_database():
    """
    This function is used to get the databse
    :return: List of two panda dataframes, one for coils and one for dummy coils
    """
    dummy_coils = pd.read_excel("default_database_dummy_coils_statictest.xlsx")
    coils = pd.read_excel("default_database_statictest.xlsx")
    return [coils, dummy_coils]

# test MS Access Drivers availability for Python
# msa_drivers = [x for x in pyodbc.drivers() if 'ACCESS' in x.upper()]
# print(f'MS-Access Drivers : {msa_drivers}')
# make sure, that "Microsoft Access Driver (*.mdb, *.accdb)" is part of the drivers

def get_coils_from_database_new():
    """
    This function is used to get the databse from MS Access
    :return: List of two panda dataframes, one for coils and one for dummy coils
    """

    # Establish Database Connection in MS Access
    # CoilsDatabase includes default data and dummy coils
    try:
        con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Patrick\Documents\Schule\Master\Kurse\IT-Systeme und IT-Projektmanagement\Projekt\Code\Materialreihenfolge_Stahl_IT_Systeme\MATERIALREIHENFOLGE_STAHL\REIHENFOLGE_APP\CoilsDatabase.accdb;'
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

def generate_path(coils, dummy_coils, tolerance_h_per, tolerance_w_abs):
    """
    This function compares the number of dummy coils for different path-finding algorithms and returns the complete coil
    list of the path with the lowest number of dummy coils.
    :param coils:
    :param dummy_coils:
    :param tolerance_h_per:
    :param tolerance_w_abs:
    :return:
    """
    # ToDo: Raise Error when it's not possible to create a fusible path with one of the algorithms

    # Path Option 1:
    #   - Sort coil list based on hight + width
    coils_path1 = coils.sort_values(by=['Hight','Width'], ignore_index=True)
    complete_coil_list_path1 = get_complete_coil_list(coils_path1, dummy_coils, tolerance_h_per, tolerance_w_abs)

    # Path Option 2:
    #   - Sort coil list based on width + hight
    coils_path2 = coils.sort_values(by=['Width','Hight'], ignore_index=True)
    complete_coil_list_path2 = get_complete_coil_list(coils_path2, dummy_coils, tolerance_h_per, tolerance_w_abs)

    # Checke ob Pfade möglich sind
    if not isinstance(coils_path1, pd.DataFrame): # Pfad 1 nicht möglich
        if isinstance(coils_path2, pd.DataFrame): # Pfad 1 nicht möglich, Pfad 2 möglich
            return complete_coil_list_path2
        else:   # Pfad 1 und Pfad 2 nicht möglich
            return -1
    else:   # Pfad 1 möglich
        if not isinstance(coils_path2, pd.DataFrame):   # Pfad 2 nicht möglich
            return complete_coil_list_path1
        else:   # Pfad 1 und Pfad 2 möglich: Verwende Pfad mit weniger Dummy-Coils
            if(len(complete_coil_list_path1[complete_coil_list_path1['dummy'] == True]) < len(complete_coil_list_path2[complete_coil_list_path2['dummy'] == True])):
                return complete_coil_list_path1
            else:
                return complete_coil_list_path2

def get_complete_coil_list(coils, dummy_coils, tolerance_h_per, tolerance_w_abs):
    """
    This function gets the complete coil list for a selected path of coils (as sorted in the given "coil" parameter),
    including dummy-coils.
    :param coils:
    :param dummy_coils:
    :param tolerance_h_per:
    :param tolerance_w_abs:
    :return:
    """

    # Add additional rows to coils pandas dataframe
    # tolerance_h, h_min, h_max
    coils['tolerance_h'] = tolerance_h_per/100*coils.Hight
    coils['tolerance_h_bottom'] = coils.Hight-coils.tolerance_h # ToDo: negative = 0 setzen
    coils['tolerance_h_top'] = coils.Hight+coils.tolerance_h
    # tolerance_w, w_min, w_max
    coils['tolerance_w'] = tolerance_w_abs
    coils['tolerance_w_bottom'] = coils.Width-coils.tolerance_w # ToDo: negative = 0 setzen
    coils['tolerance_w_top'] = coils.Width+coils.tolerance_w
    coils['dummy'] = False

    # Add additional rows to dummy_coils pandas dataframe
    # tolerance_h, h_min, h_max
    dummy_coils['tolerance_h'] = tolerance_h_per/100*dummy_coils.Hight
    dummy_coils['tolerance_h_bottom'] = dummy_coils.Hight-dummy_coils.tolerance_h # ToDo: negative = 0 setzen
    dummy_coils['tolerance_h_top'] = dummy_coils.Hight+dummy_coils.tolerance_h
    # tolerance_w, w_min, w_max
    dummy_coils['tolerance_w'] = tolerance_w_abs
    dummy_coils['tolerance_w_bottom'] = dummy_coils.Width-dummy_coils.tolerance_w # ToDo: negative = 0 setzen
    dummy_coils['tolerance_w_top'] = dummy_coils.Width+dummy_coils.tolerance_w
    dummy_coils['dummy'] = True

    complete_coils = coils.iloc[[0]]
    for n in range(len(coils)-1):
        # Nächstes coil liegt im Toleranzbereich:
        if (coils.tolerance_h_top[n] >= coils.Hight[n+1] >= coils.tolerance_h_bottom[n]) and (
                coils.tolerance_w_top[n] >= coils.Width[n+1] >= coils.tolerance_w_bottom[n]):
            complete_coils = complete_coils.append(coils.iloc[n+1], ignore_index=True)
        # Nächstes Coil liegt nicht im Toleranzbereich: Dummycoil(s) notwendig
        else:
            dummy_coils_selection = get_dummy_coils(coils.iloc[[n]],coils.iloc[[n+1]], dummy_coils)
            if not isinstance(dummy_coils_selection, pd.DataFrame):
                return -1
            complete_coils = complete_coils.append(dummy_coils_selection)
            complete_coils = complete_coils.append(coils.iloc[n+1], ignore_index=True)

    # Clean not needed parameters from pandas dataframe
    complete_coils = complete_coils[['RecordID', 'Hight', 'Width', 'dummy']]
    return complete_coils

def get_dummy_coils(coil1, coil2, dummy_coils):
    """
    This function searches for needed dummy_coils to be able to fuse coil1 with coil2.
    :param coil1:
    :param coil2:
    :param dummy_coils:
    :return:
    """

    dummy_coils_rslt = dummy_coils
    # Check hight:
    # Hight von coil2 im Toleranzbereich von coil1
    if (coil1.tolerance_h_top.iloc[0] >= coil2.Hight.iloc[0] >= coil1.tolerance_h_bottom.iloc[0]):
        dummy_coils_rslt = dummy_coils_rslt[(coil1.tolerance_h_top.iloc[0] >= dummy_coils_rslt['Hight']) & (dummy_coils_rslt['Hight'] >= coil1.tolerance_h_bottom.iloc[0])]
        dummy_coils_rslt = dummy_coils_rslt[(dummy_coils_rslt['tolerance_h_top'] >= coil2.Hight.iloc[0]) & (coil2.Hight.iloc[0] >= dummy_coils_rslt['tolerance_h_bottom'])]
    # Hight von coil2 außerhalb Toleranzbereich von coil1
    else:
        if coil1.Hight.iloc[0] > coil2.Hight.iloc[0]:
            dummy_coils_rslt = dummy_coils_rslt[dummy_coils_rslt['Hight'] >= coil1.tolerance_h_bottom.iloc[0]]
            # Sortieren und somit dummy_coil auswählen was am nähsten an Toleranzgrenze liegt
            #dummy_coils_rslt = dummy_coils_rslt.sort_values(by=['Hight'])
        else: # coil1.Hight.iloc[0] < coil2.Hight.iloc[0]:
            dummy_coils_rslt = dummy_coils_rslt[dummy_coils_rslt['Hight'] <= coil1.tolerance_h_top.iloc[0]]
            # Sortieren und somit dummy_coil auswählen was am nähsten an Toleranzgrenze liegt
            #dummy_coils_rslt = dummy_coils_rslt.sort_values(by=['Hight'], ascending=False)

    # Check width:
    # Width von coil2 im Toleranzbereich von coil1
    if (coil1.tolerance_w_top.iloc[0] >= coil2.Width.iloc[0] >= coil1.tolerance_w_bottom.iloc[0]):
        dummy_coils_rslt = dummy_coils_rslt[(coil1.tolerance_w_top.iloc[0] >= dummy_coils_rslt['Width']) & (dummy_coils_rslt['Width'] >= coil1.tolerance_w_bottom.iloc[0])]
        dummy_coils_rslt = dummy_coils_rslt[(dummy_coils_rslt['tolerance_w_top'] >= coil2.Width.iloc[0]) & (coil2.Width.iloc[0] >= dummy_coils_rslt['tolerance_w_bottom'])]
    # Width von coil2 außerhalb Toleranzbereich von coil1
    else:
        if coil1.Width.iloc[0] > coil2.Width.iloc[0]:
            dummy_coils_rslt = dummy_coils_rslt[dummy_coils_rslt['Width'] >= coil1.tolerance_w_bottom.iloc[0]]
            # Sortieren und somit dummy_coil auswählen was am nähsten an Toleranzgrenze liegt
            #dummy_coils_rslt = dummy_coils_rslt.sort_values(by=['Width'])
        else:  # coil1.Width.iloc[0] < coil2.Width.iloc[0]:
            dummy_coils_rslt = dummy_coils_rslt[dummy_coils_rslt['Width'] <= coil1.tolerance_w_top.iloc[0]]
            # Sortieren und somit dummy_coil auswählen was am nähsten an Toleranzgrenze liegt
            #dummy_coils_rslt = dummy_coils_rslt.sort_values(by=['Width'], ascending=False)

    # Sortieren: Dummy-Coils auswählen die am nächsten an Toleranzgrenze liegen
    if coil1.Hight.iloc[0] > coil2.Hight.iloc[0]:
        if coil1.Width.iloc[0] > coil2.Width.iloc[0]:
            dummy_coils_rslt = dummy_coils_rslt.sort_values(by=['Hight','Width'], ascending=[True, True], ignore_index=True)
        else:
            dummy_coils_rslt = dummy_coils_rslt.sort_values(by=['Hight','Width'], ascending=[True, False], ignore_index=True)
    else:
        if coil1.Width.iloc[0] > coil2.Width.iloc[0]:
            dummy_coils_rslt = dummy_coils_rslt.sort_values(by=['Hight','Width'], ascending =[False, True], ignore_index=True)
        else:
            dummy_coils_rslt = dummy_coils_rslt.sort_values(by=['Hight','Width'], ascending =[False, False], ignore_index=True)

    # Wähle erstes Dummy-Coil (alle Coils aus Liste passen, aber das erste stellt das sinnvollste Coil dar)
    dummy_coils_rslt = dummy_coils_rslt.iloc[[0]]
    # Neues Dummycoil entspricht dem vorherigen Dummycoil -> Keine passenden Dummycoils zur Überbrückung vorhanden
    if coil1.Hight.iloc[0] == dummy_coils_rslt.Hight.iloc[0] & coil1.Hight.iloc[0] == dummy_coils_rslt.Hight.iloc[0] & coil1.dummy.iloc[0] == True:
            return -1
    # Coil2 (End-Coil) im Toleranzbereich vom Dummy-Coil
    if (dummy_coils_rslt.tolerance_h_top.iloc[0] >= coil2.Hight.iloc[0] >= dummy_coils_rslt.tolerance_h_bottom.iloc[0]) and (dummy_coils_rslt.tolerance_w_top.iloc[0] >= coil2.Width.iloc[0] >= dummy_coils_rslt.tolerance_w_bottom.iloc[0]):
        return dummy_coils_rslt
    # Coil2 (End-Coil) noch immer nicht im Toleranzbereiche vom ausgewählten Dummy-Coil
    else:
        dummy_next = get_dummy_coils(dummy_coils_rslt, coil2, dummy_coils)
        if not isinstance(dummy_next, pd.DataFrame):
            return -1
        else:
            dummy_coils_rslt = dummy_coils_rslt.append(dummy_next, ignore_index=True)

    return dummy_coils_rslt

#-----------------------------------------------------------------------------------------------------------------------


[coils, dummy_coils] = get_coils_from_database()
#[coilsnew, dummy_coilsnew] = get_coils_from_database_new()




tolerance_h_per = 10
tolerance_w_abs = 10
print('-----------------------------------------------------')
print('Eingelesene Coils:')
print(coils)
print('-----------------------------------------------------')
print('Eingelesene Dummy-Coils:')
print(dummy_coils)
print('-----------------------------------------------------')
complete_coils = generate_path(coils, dummy_coils, tolerance_h_per, tolerance_w_abs)
print('Erstellter Pfad:')
print(complete_coils[complete_coils['dummy'] == False])
print('-----------------------------------------------------')
print('Gesamt-Coilliste für gewählten Pfad:')
print(complete_coils)

#print('\n\n\n\n-----------------------------------------------------')
#print('Eingelesene Coils:')
#print(coilsnew)
#print('-----------------------------------------------------')
#print('Eingelesene Dummy-Coils:')
#print(dummy_coilsnew)
#print('-----------------------------------------------------')
#complete_coilsnew = generate_path(coilsnew, dummy_coilsnew, tolerance_h_per, tolerance_w_abs)
#print('Erstellter Pfad:')
#print(complete_coilsnew[complete_coilsnew['dummy'] == False])
#print('-----------------------------------------------------')
#print('Gesamt-Coilliste für gewählten Pfad:')
#print(complete_coilsnew)


