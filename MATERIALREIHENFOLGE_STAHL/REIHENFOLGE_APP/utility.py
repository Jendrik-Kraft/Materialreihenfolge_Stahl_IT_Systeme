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
