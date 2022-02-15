import json

from django.shortcuts import render
# Create your views here.
import random
from .database import *
from .utility import *


def mainpage(request, dicke=0, breite=0, pfade="all"):
    [coils, dummy_coils] = get_coils_from_database()
    coils = round(coils, 2)
    coil_list_for_js = build_coil_list_for_js(coils)
    fitting_coils = find_fusible_coils(coils, breite, dicke)
    fitting_coils_for_js = build_fitting_coils_list_for_js(coils, fitting_coils)
    return render(request, 'REIHENFOLGE/index.html', {"coils": coil_list_for_js, "connections": fitting_coils_for_js})


def editpage(request, table=""):
    [coils, dummy_coils] = get_coils_from_database()
    coils = round(coils, 2)
    if table:
        mylist = table.split(";")
        editedCoilArray = []
        for element in mylist:
            editedCoilArray.append(element.split(","))
        if len(editedCoilArray) > 0:
            del editedCoilArray[0]
    coil_list_for_js = build_coil_list_for_js(coils)
    return render(request, 'REIHENFOLGE/editPage.html', {"coils": coils.values.tolist()})
