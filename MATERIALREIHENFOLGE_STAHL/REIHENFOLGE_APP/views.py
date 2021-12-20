import json

from django.shortcuts import render
# Create your views here.
import random
from .database import *
from .utility import *


def hi(request):
    [coils, dummy_coils] = get_coils_from_database()
    coil_list_for_js = build_coil_list_for_js(coils)
    fitting_coils = find_fusible_coils(coils, 30, 100)  # TODO Use parameters from URL to configure tolerances
    fitting_coils_for_js = build_fitting_coils_list_for_js(coils, fitting_coils)
    return render(request, 'REIHENFOLGE/graph_try.html', {"coils": coil_list_for_js, "connections": fitting_coils_for_js})

