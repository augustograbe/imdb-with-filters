from django.urls import path
from django.conf.urls import handler404

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("rank_diretor", views.rank_diretor, name="rank_diretor"),
    path("rank_ator", views.rank_ator, name="rank_ator"),
    path("rank_roteirista", views.rank_roterista, name="rank_roteirista"),
    path("filme/<str:filme_id>", views.filme, name="filme"),
    path("pessoa/<str:pessoa_id>", views.pessoa, name="pessoa"),
    path("pesquisa/", views.pesquisa, name="pesquisa"),
    path("login", views.login, name="login"),
    path("registrar", views.registrar, name="registrar"),
    path("logout", views.logout, name="logout"),
    path("favoritos", views.favoritos, name="favoritos")
]

handler404 = ""