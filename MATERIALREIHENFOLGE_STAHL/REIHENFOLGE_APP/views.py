from django.shortcuts import render
# Create your views here.
import random
from .database import *
from .utility import *
def hi(request):
    [coils, dummy_coils] = get_coils_from_database()
    coils_list = coils.values.tolist()
    liste_for_js = []
    for coil in coils_list:
        liste_for_js.append({"x":coil[1], "y":coil[2]})
    print(liste_for_js)
    fitting_coils = find_fusible_coils(coils, 10, 50)
    return render(request, 'REIHENFOLGE/graph_try.html', {"name": liste_for_js, "number": random.randint(0,1100)})
