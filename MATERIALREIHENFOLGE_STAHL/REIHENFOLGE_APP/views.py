import django.template
from django.shortcuts import render
from .database import *
from .utility import *


# Create your views here.
def mainpage(request, dicke=0, breite=0, pfade="all"):
    dummy_coils_for_js = []
    [coils, dummy_coils] = get_coils_from_database()
    error = 0
    if pfade == "all":
        fitting_coils = find_fusible_coils(coils, breite, dicke)
        fitting_coils_for_js = build_fitting_coils_list_for_js(coils, fitting_coils)
        dummy_coils_for_js = build_coil_list_for_js(dummy_coils)

    # if both tolerances are 0, generate_path will error. Thus we only execute it if tolerances are given
    if pfade == "best_path" and (dicke != 0 or breite != 0):
        complete_coils = generate_path(coils, dummy_coils, dicke, breite)
        if type(complete_coils) is int:  # Rückgabe -1 -> es wurde kein Pfad gefunden
            fitting_coils = find_fusible_coils(coils, 0, 0)
            fitting_coils_for_js = build_fitting_coils_list_for_js(coils, fitting_coils)
            error = 1
            #dummy_coils_for_js = build_coil_list_for_js(dummy_coils)
        else:
            #fitting_coils = find_fusible_coils(coils, breite, dicke)
            dummy_coils_for_js = build_dummy_coil_list_for_js(complete_coils)
            fitting_coils_for_js = build_path_for_js(complete_coils)
    elif pfade == "best_path":
        fitting_coils = find_fusible_coils(coils, 0, 0)
        fitting_coils_for_js = build_fitting_coils_list_for_js(coils, fitting_coils)
    coil_list_for_js = build_coil_list_for_js(coils)
    return render(request, 'REIHENFOLGE/index.html', {"coils": coil_list_for_js, "connections": fitting_coils_for_js,
                                                      "dummy_coils": dummy_coils_for_js, "error": error })


def editpage(request, breiteOrId=0, dicke=0):
    if dicke != 0:
        new_coil = (dicke, breiteOrId)
        add_coils_to_database(new_coil)
    else:
        delete_coils_from_database(breiteOrId)
    [coils, dummy_coils] = get_coils_from_database()
    coils = round(coils, 2)
    coil_list_for_js = build_coil_list_for_js(coils)
    return render(request, 'REIHENFOLGE/editPage.html', {"coils": coils.values.tolist()})
