from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection

from bs4 import BeautifulSoup
from urllib.request import urlopen

from .models import Filme, Pessoa, Titulo, Genero, Avaliacao, Ator, Diretor, Roterista, Elenco,  TrabalhouComo, ConhecidoPor
# Create your views here.

# Acha o link da imagem da capa do filme
def imagem_capa(title_id):
  title_url = f'https://www.imdb.com/title/{title_id}/'
  html = urlopen(title_url)
  bs = BeautifulSoup(html,"html.parser")
  data = bs.find('div',{'class':'ipc-poster'})
  poster_link = data.img['src']
  return poster_link
  



#Tranformar os reultados das querys em dicionários
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def rank_dict(dict):
    i=1
    for filme in dict:
        filme['rank'] = i
        i += 1
    return dict


# --------------Paginas-----------------
def index(request):
    filtros = {}
    query_from = request.GET.get("fromInput","")
    if query_from == "": query_from = "1911"
    print(f"")
    filtros['from'] = query_from
    query_to = request.GET.get("toInput","")
    if query_to == "": query_to= "2022"
    filtros['to'] = query_to
    query_nota = request.GET.get("notaInput","")
    if query_nota == "": query_nota= "0"
    filtros['nota'] = query_nota
    query_votos = request.GET.get("qtd_votos","")
    if query_votos== "": query_votos = "30000"
    filtros['votos'] = query_votos

    selecao = (f"SELECT distinct filme.filme_id, titulo_primario, lancamento, nota_media, num_votos FROM filme, avaliacao, genero WHERE filme.filme_id = avaliacao.filme_id  AND filme.filme_id=genero.filme_id AND lancamento BETWEEN {query_from} AND {query_to} AND num_votos > {query_votos} AND nota_media > {query_nota} ORDER BY nota_media  desc limit 250")
    #------------Generos--------------
    
    query = request.GET.get("acao","")
    if query == "1":
        filtros['acao'] = "checked"
    query = request.GET.get("aventura","")
    if query == "1":
        filtros['aventura'] = "checked"
    query = request.GET.get("animacao","")
    if query == "1":
        filtros['animacao'] = "checked"
    query = request.GET.get("biografia","")
    if query == "1":
        filtros['biografia'] = "checked"
    query = request.GET.get("comedia","")
    if query == "1":
        filtros['comedia'] = "checked"
    query = request.GET.get("crime","")
    if query == "1":
        filtros['crime'] = "checked"
    query = request.GET.get("crime","")
    if query == "1":
        filtros['crime'] = "checked"
    query = request.GET.get("documentario","")
    if query == "1":
        filtros['documentario'] = "checked"
    query = request.GET.get("drama","")
    if query == "1":
        filtros['drama'] = "checked"
    query = request.GET.get("familia","")
    if query == "1":
        filtros['familia'] = "checked"
    query = request.GET.get("fantasia","")
    if query == "1":
        filtros['fantasia'] = "checked"
    query = request.GET.get("horror","")
    if query == "1":
        filtros['horror'] = "checked"
    query = request.GET.get("historico","")
    if query == "1":
        filtros['historico'] = "checked"
    query = request.GET.get("misterio","")
    if query == "1":
        filtros['misterio'] = "checked"
    query = request.GET.get("romance","")
    if query == "1":
        filtros['romance'] = "checked"
    query = request.GET.get("cientifica","")
    if query == "1":
        filtros['cientifica'] = "checked"
    query = request.GET.get("esporte","")
    if query == "1":
        filtros['esporte'] = "checked"
    query = request.GET.get("suspense","")
    if query == "1":
        filtros['suspense'] = "checked"
    query = request.GET.get("guerra","")
    if query == "1":
        filtros['guerra'] = "checked"
    query = request.GET.get("faroeste","")
    if query == "1":
        filtros['faroeste'] = "checked"
    
    

    cursor = connection.cursor()
    cursor.execute(selecao)
    filmes = dictfetchall(cursor)
    filmes = rank_dict(filmes)
    return render(request, "imdb_filmes/index.html",{
        "filmes": filmes,
        "filtros": filtros
    })

def rank_diretor(request):
    return render(request, "imdb_filmes/rank_diretor.html")

def rank_ator(request):
    return render(request, "imdb_filmes/rank_ator.html")

def rank_roterista(request):
    return render(request, "imdb_filmes/rank_roteirista.html")

def filme(request, filme_id):
    cursor = connection.cursor()
    cursor.execute(f"SELECT filme_id, titulo_primario, titulo_original, lancamento, tempo FROM filme WHERE filme_id='{filme_id}'")
    filme = dictfetchall(cursor)
    cursor.execute(f"SELECT nota_media, num_votos FROM avaliacao WHERE filme_id='{filme_id}'")
    avaliacao = dictfetchall(cursor)
    cursor.execute(f"SELECT pessoa.pessoa_id, nome FROM pessoa, roterista WHERE pessoa.pessoa_id=roterista.pessoa_id AND filme_id='{filme_id}'")
    roteiristas = dictfetchall(cursor)
    cursor.execute(f"SELECT pessoa.pessoa_id, nome FROM pessoa, diretor WHERE pessoa.pessoa_id=diretor.pessoa_id AND filme_id='{filme_id}'")
    diretores = dictfetchall(cursor)
    cursor.execute(f"SELECT pessoa.pessoa_id, nome FROM pessoa, ator WHERE pessoa.pessoa_id=ator.pessoa_id AND filme_id='{filme_id}'")
    atores = dictfetchall(cursor)
    cursor.execute(f"SELECT genero FROM genero WHERE filme_id='{filme_id}'")
    generos = dictfetchall(cursor)
    capa = imagem_capa(filme_id)
    return render(request, "imdb_filmes/filme.html", {
        "filme": filme,
        "avaliacao": avaliacao,
        "roteiristas": roteiristas,
        "diretores": diretores,
        "atores": atores,
        "generos": generos,
        "capa": capa
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