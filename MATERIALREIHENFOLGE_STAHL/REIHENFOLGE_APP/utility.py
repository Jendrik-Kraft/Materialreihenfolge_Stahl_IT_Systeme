import json


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


def build_coil_list_for_js(coils):
    """
    This function converts the coils to the right format for javascript code
    :param coils: Panda data frame of all coils that should be shown
    :return: The same data but in the right format
    """
    coils_list = coils.values.tolist()
    list_for_js = []
    for coil in coils_list:
        list_for_js.append({"x": coil[1], "y": coil[2]})
    list_for_js = json.dumps(list_for_js)
    return list_for_js


def build_dummy_coil_list_for_js(complete_coils):
    """
    This function converts the necessary dummy_coils to the right format for javascript code
    :param complete_coils: Panda data frame of all coils that should be shown
    :return: The only dummy_coils in right format
    """
    coils_list = complete_coils.values.tolist()
    list_for_js = []
    for coil in coils_list:
        if coil[3] is True:
            list_for_js.append({"x": coil[1], "y": coil[2]})
    list_for_js = json.dumps(list_for_js)
    return list_for_js


def build_path_for_js(complete_coils):
    path_for_js = []
    coils_list = complete_coils.values.tolist()
    n=0
    while n < len(coils_list)-1:
        path_for_js.append({"x": coils_list[n][1], "y": coils_list[n][2]})
        path_for_js.append({"x": coils_list[n+1][1], "y": coils_list[n+1][2]})
        path_for_js.append({"x": None, "y": None})
        n=n+1
    path_for_js = json.dumps(path_for_js)
    return path_for_js


def build_fitting_coils_list_for_js(coils, fitting_coils):
    """
    This function converts the found pairs that need to be connected to the right format for javascript code
    :param coils: Panda data frame of all coils that will be shown
    :param fitting_coils: List of coils that need to be connected in the graph
    :return: A list of the coordinated that need to be connected in the right format for javascript code
    """
    coils_list = coils.values.tolist()
    fitting_coils_for_js = []
    for pair in fitting_coils:
        index = coils.loc[coils['RecordID'] == pair[0]]
        index_list = index.values.tolist()
        fitting_coils_for_js.append({"x": index_list[0][1], "y": index_list[0][2]})
        index = coils.loc[coils['RecordID'] == pair[1]]
        index_list = index.values.tolist()
        fitting_coils_for_js.append({"x": index_list[0][1], "y": index_list[0][2]})
        fitting_coils_for_js.append({"x": None, "y": None})
    fitting_coils_for_js = json.dumps(fitting_coils_for_js)
    return fitting_coils_for_js


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
    # ToDo: Raise Error when it's not possible to create a fusible coil-list

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
            complete_coils = complete_coils.append(get_dummy_coils(coils.iloc[[n]],coils.iloc[[n+1]], dummy_coils))
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
    # ToDo: Raise Error when it's not possible to fuse 2 coils with given dummy-coils
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

    # Wähle erstes Dummy-Coil (alle Coils aus Liste passen, aber das erste stellt das sinnvolste Coil dar)
    dummy_coils_rslt = dummy_coils_rslt.iloc[[0]]
    # Coil2 (End-Coil) im Toleranzbereich vom Dummy-Coil
    if (dummy_coils_rslt.tolerance_h_top.iloc[0] >= coil2.Hight.iloc[0] >= dummy_coils_rslt.tolerance_h_bottom.iloc[0]) and (dummy_coils_rslt.tolerance_w_top.iloc[0] >= coil2.Width.iloc[0] >= dummy_coils_rslt.tolerance_w_bottom.iloc[0]):
        return dummy_coils_rslt
    # Coil2 (End-Coil) noch immer nicht im Toleranzbereiche vom ausgewählten Dummy-Coil
    else:
        dummy_coils_rslt = dummy_coils_rslt.append(get_dummy_coils(dummy_coils_rslt, coil2, dummy_coils), ignore_index=True)

    return dummy_coils_rslt
