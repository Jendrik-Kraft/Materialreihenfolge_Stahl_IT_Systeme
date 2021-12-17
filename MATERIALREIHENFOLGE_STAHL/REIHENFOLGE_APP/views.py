from django.shortcuts import render
# Create your views here.
import random

def hi(request):

    return render(request, 'REIHENFOLGE/graph_try.html', {"name": random.randint(0,100), "number": random.randint(0,1100)})
