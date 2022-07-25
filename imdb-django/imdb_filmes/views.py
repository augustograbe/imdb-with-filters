from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection

from .models import Filme, Pessoa, Titulo, Genero, Avaliacao, Ator, Diretor, Roterista, Elenco,  TrabalhouComo, ConhecidoPor
# Create your views here.


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]




# Paginas
def index(request):
    return render(request, "imdb_filmes/index.html",{
        "Filmes": Filme.objects.raw('SELECT titulo_primario, lancamento FROM filme LIMIT 250')
    })

def rank_diretor(request):
    return render(request, "imdb_filmes/rank_diretor.html")

def rank_ator(request):
    return render(request, "imdb_filmes/rank_ator.html")

def rank_roterista(request):
    return render(request, "imdb_filmes/rank_roterista.html")

def filme(request, filme_id):
 #  filme = Filme.objects.get(pk=filme_id)
 #   filme = Filme.objects.raw("SELECT * FROM filme WHERE filme_id = '%s' LIMIT 1", [filme_id])
    cursor = connection.cursor()
    cursor.execute("SELECT titulo_primario, lancamento FROM filme WHERE filme_id='%s'", [filme_id])
    filme = dictfetchall(cursor)
    return render(request, "imdb_filmes/filme.html", {
        "filme": filme
    } )

def pessoa(request, name):
    return render(request, "imdb_filmes/pessoa.html", {
        
    } )

def pesquisa(request):
        return render(request, "imdb_filmes/pesquisa.html", {
        
    } )