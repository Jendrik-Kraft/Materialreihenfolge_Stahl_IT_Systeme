import django.template
from django.shortcuts import render
from .database_xlsx_old import *
from .utility import *

# Create your views here.
def mainpage(request, dicke=0, breite=0, pfade="all"):

    dummy_coils_for_js = []
    [coils, dummy_coils] = get_coils_from_database()

    if pfade == "all":
        fitting_coils = find_fusible_coils(coils, breite, dicke)
        fitting_coils_for_js = build_fitting_coils_list_for_js(coils, fitting_coils)
        dummy_coils_for_js = build_coil_list_for_js(dummy_coils)

    # if both tolerances are 0, generate_path will error. Thus we only execute it if tolerances are given
    if pfade == "best_path" and (dicke != 0 or breite != 0):
        complete_coils = generate_path(coils, dummy_coils, breite, dicke)
        if type(complete_coils) is int:
            fitting_coils = find_fusible_coils(coils, 0, 0)
            fitting_coils_for_js = build_fitting_coils_list_for_js(coils, fitting_coils)
            #dummy_coils_for_js = build_coil_list_for_js(dummy_coils)
        else:
            #fitting_coils = find_fusible_coils(coils, breite, dicke)
            dummy_coils_for_js = build_dummy_coil_list_for_js(complete_coils)
            fitting_coils_for_js = build_path_for_js(complete_coils)
    coil_list_for_js = build_coil_list_for_js(coils)
    return render(request, 'REIHENFOLGE/index.html', {"coils": coil_list_for_js, "connections": fitting_coils_for_js,
                                                      "dummy_coils": dummy_coils_for_js})


def editpage(request, table=""):
    [coils, dummy_coils] = get_coils_from_database()
    coils = round(coils, 2)
    table = table;
    coil_list_for_js = build_coil_list_for_js(coils)
    return render(request, 'REIHENFOLGE/editPage.html', {"coils": coils.values.tolist()})
