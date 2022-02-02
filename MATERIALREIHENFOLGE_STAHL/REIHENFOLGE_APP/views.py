import json

from django.shortcuts import render
# Create your views here.
import random
from .database import *
from .utility import *


def hi(request, dicke=0, breite=0, pfade="all"):
    dummy_coils_for_js = []
    [coils, dummy_coils] = get_coils_from_database()
    # if both tolerances are 0, generate_path will error. Thus we only execute it if tolerances are given
    if dicke != 0 or breite != 0:
        complete_coils = generate_path(coils, dummy_coils, breite, dicke)
        fitting_coils = find_fusible_coils(coils, breite, dicke)
        dummy_coils_for_js = build_dummy_coil_list_for_js(complete_coils)
    else:
        fitting_coils = find_fusible_coils(coils, breite, dicke)
        complete_coils = coils

    coil_list_for_js = build_coil_list_for_js(coils)
    fitting_coils_for_js = build_fitting_coils_list_for_js(coils, fitting_coils)
    print(complete_coils)
    path = build_path_for_js(complete_coils)
    return render(request, 'REIHENFOLGE/index.html', {"coils": coil_list_for_js, "connections": fitting_coils_for_js,
                                                      "dummy_coils": dummy_coils_for_js})
