from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection

from .models import Filme, Pessoa, Titulo, Genero, Avaliacao, Ator, Diretor, Roterista, Elenco,  TrabalhouComo, ConhecidoPor
# Create your views here.

#Tranformar os reultados das querys em dicionários
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]




# Paginas
def index(request):
    cursor = connection.cursor()
    cursor.execute("SELECT filme.filme_id, titulo_primario, lancamento, nota_media, num_votos FROM filme, avaliacao WHERE filme.filme_id = avaliacao.filme_id  ORDER BY nota_media  desc limit 250")
    filmes = dictfetchall(cursor)
    return render(request, "imdb_filmes/index.html",{
        "filmes": filmes
    })

def rank_diretor(request):
    return render(request, "imdb_filmes/rank_diretor.html")

def rank_ator(request):
    return render(request, "imdb_filmes/rank_ator.html")

def rank_roterista(request):
    return render(request, "imdb_filmes/rank_roterista.html")

def filme(request, filme_id):
    cursor = connection.cursor()
    cursor.execute(f"SELECT titulo_primario, titulo_original, lancamento, tempo FROM filme WHERE filme_id='{filme_id}'")
    filme = dictfetchall(cursor)
    print(filme)
    print(connection.queries)
    return render(request, "imdb_filmes/filme.html", {
        "filme": filme
    } )

def pessoa(request, pessoa_id):
    cursor = connection.cursor()
    cursor.execute(f"SELECT nome, nascimento, morte from pessoa WHERE pessoa_id='{pessoa_id}'")
    pessoa = dictfetchall(cursor)
    return render(request, "imdb_filmes/pessoa.html", {
        "pessoa": pessoa
    } )

def pesquisa(request):
        return render(request, "imdb_filmes/pesquisa.html", {
        
    } )