from django.urls import path
from django.conf.urls import handler404

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("filme/<str:entry>", views.filme, name="filme"),
    path("search/", views.search, name="search"),
]

handler404 = ""