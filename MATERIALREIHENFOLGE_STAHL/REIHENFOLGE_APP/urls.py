"""MATERIALREIHENFOLGE_STAHL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage, name="home-page"),
    path('display_graph/<int:breite>/<int:dicke>/<str:pfade>', views.mainpage, name="home-page"),
    path('display_graph/<int:breite>/<int:dicke>', views.mainpage, name="home-page"),
    path('edit_database/test', views.editpage, name="edit-page"),
    path('edit_database/test/<int:breiteOrId>/<int:dicke>', views.editpage, name="edit-page"),
    path('edit_database/test/<int:breiteOrId>', views.editpage, name="edit-page"),
]
