from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "imdb_filmes/index.html")

def rank_diretor(request):
    return render(request, "imdb_filmes/rank_diretor.html")

def rank_ator(request):
    return render(request, "imdb_filmes/rank_ator.html")

def rank_roterista(request):
    return render(request, "imdb_filmes/rank_roterista.html")

def filme(request, name):
    return render(request, "imdb_filmes/filme.html", {

    } )

def pessoa(request, name):
    return render(request, "imdb_filmes/pessoa.html", {
        
    } )

def pesquisa(request):
        return render(request, "imdb_filmes/pesquisa.html", {
        
    } )