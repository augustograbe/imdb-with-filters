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
    filtros['from'] = query_from
    query_to = request.GET.get("toInput","")
    if query_to == "": query_to= "2022"
    filtros['to'] = query_to
    query_nota = request.GET.get("notaInput","")
    if query_nota == "": query_nota= "0"
    filtros['nota'] = query_nota
    query_votos = request.GET.get("qtd_votos","")
    if query_votos== "": query_votos = "50000"
    filtros['votos'] = query_votos

    selecao = (f"SELECT distinct filme.filme_id, titulo_primario, lancamento, nota_media, num_votos, url FROM filme, avaliacao, genero, capa WHERE filme.filme_id = avaliacao.filme_id  AND filme.filme_id=genero.filme_id AND filme.filme_id=capa.filme_id AND lancamento BETWEEN {query_from} AND {query_to} AND num_votos > {query_votos} AND nota_media > {query_nota} ")
    
    #------------Generos--------------
    selecao += ("AND genero IN (''")
    query = request.GET.get("acao","")
    if query != "0":
        filtros['acao'] = "checked"
        selecao += (",'Action'")
    query = request.GET.get("aventura","")
    if query != "0":
        filtros['aventura'] = "checked"
        selecao += (",'Adventure'")
    query = request.GET.get("animacao","")
    if query != "0":
        filtros['animacao'] = "checked"
        selecao += (",'Animation'")
    query = request.GET.get("biografia","")
    if query != "0":
        filtros['biografia'] = "checked"
        selecao += (",'Biography'")
    query = request.GET.get("comedia","")
    if query != "0":
        filtros['comedia'] = "checked"
        selecao += (",'Comedy'")
    query = request.GET.get("crime","")
    if query != "0":
        filtros['crime'] = "checked"
        selecao += (",'Crime'")
    query = request.GET.get("documentario","")
    if query == "1":
        filtros['documentario'] = "checked"
        selecao += (",'Documentary'")
    query = request.GET.get("drama","")
    if query != "0":
        filtros['drama'] = "checked"
        selecao += (",'Drama'")
    query = request.GET.get("familia","")
    if query != "0":
        filtros['familia'] = "checked"
        selecao += (",'Family'")
    query = request.GET.get("fantasia","")
    if query != "0":
        filtros['fantasia'] = "checked"
        selecao += (",'Fantasy'")
    query = request.GET.get("horror","")
    if query != "0":
        filtros['horror'] = "checked"
        selecao += (",'Horror'")
    query = request.GET.get("historico","")
    if query != "0":
        filtros['historico'] = "checked"
        selecao += (",'History'")
    query = request.GET.get("musical","")
    if query != "0":
        filtros['musical'] = "checked"
        selecao += (",'Musical'")
    query = request.GET.get("musica","")
    if query != "0":
        filtros['musica'] = "checked"
        selecao += (",'Music'")
    query = request.GET.get("misterio","")
    if query != "0":
        filtros['misterio'] = "checked"
        selecao += (",'Mystery'")
    query = request.GET.get("romance","")
    if query != "0":
        filtros['romance'] = "checked"
        selecao += (",'Romance'")
    query = request.GET.get("cientifica","")
    if query != "0":
        filtros['cientifica'] = "checked"
        selecao += (",'Sci-Fi'")
    query = request.GET.get("esporte","")
    if query != "0":
        filtros['esporte'] = "checked"
        selecao += (",'Sport'")
    query = request.GET.get("suspense","")
    if query != "0":
        filtros['suspense'] = "checked"
        selecao += (",'Thriller'")
    query = request.GET.get("guerra","")
    if query != "0":
        filtros['guerra'] = "checked"
        selecao += (",'War'")
    query = request.GET.get("faroeste","")
    if query != "0":
        filtros['faroeste'] = "checked"
        selecao += (",'Western'")
    
    selecao += (") ORDER BY nota_media  desc limit 250")

    cursor = connection.cursor()
    cursor.execute(selecao)
    filmes = dictfetchall(cursor)
    filmes = rank_dict(filmes)
    return render(request, "imdb_filmes/index.html",{
        "filmes": filmes,
        "filtros": filtros
    })

def rank_diretor(request):
    filtros = {}
    query_qtd_dirigidos = request.GET.get("qtd_dirigidos","")
    if query_qtd_dirigidos == "": query_qtd_dirigidos = "2"
    filtros['qtd_dirigidos'] = query_qtd_dirigidos
    query_votos = request.GET.get("qtd_votos","")
    if query_votos == "": query_votos = "30000"
    filtros['votos'] = query_votos
    query_vivo = request.GET.get("vivo","")
    if query_vivo == "1":
        filtros["vivo"] = "checked"
        query_vivo = ("AND morte is NULL ")
    query_rank = request.GET.get("ordem","")
    if query_rank == "media" or query_rank == "":
        rankear = ("media")
        filtros['selected'] = "media"
    elif query_rank == "ponderada":
        rankear = ("ponderada")
        filtros['selected'] = "ponderada"
    elif query_rank == "qtd_top250":
        rankear = ("num_top250")
        filtros['selected'] = "qtd_top250"
    elif query_rank == "qtd_filmes":
        rankear = ("num_filmes")
        filtros['selected'] = "qtd_filmes"

    selecao =  (f"SELECT pessoa_id, nome, ROUND(nota_media, 1) as media, ROUND(nota_ponderada, 1) as ponderada, num_filmes, num_top250, url FROM (SELECT pessoa_id, nome, AVG(nota_media) AS nota_media, SUM(nota_media * num_votos) / SUM(num_votos) AS nota_ponderada, COUNT(DISTINCT filme_id) AS num_filmes, COUNT(nm) AS num_top250, url FROM pessoa NATURAL JOIN diretor NATURAL JOIN foto NATURAL JOIN avaliacao NATURAL LEFT JOIN (SELECT filme_id, nota_media AS nm FROM TOP250) AS top250filmes WHERE num_votos > {query_votos} {query_vivo}GROUP BY nome) AS resultado WHERE num_filmes > {query_qtd_dirigidos} ORDER BY {rankear} DESC")

    cursor = connection.cursor()
    cursor.execute(selecao)
    diretores = dictfetchall(cursor)
    diretores = rank_dict(diretores)
    return render(request, "imdb_filmes/rank_diretor.html",{
        "diretores": diretores,
        "filtros": filtros
    })

def rank_ator(request):
    filtros = {}
    query_qtd_dirigidos = request.GET.get("qtd_dirigidos","")
    if query_qtd_dirigidos == "": query_qtd_dirigidos = "2"
    filtros['qtd_dirigidos'] = query_qtd_dirigidos
    query_votos = request.GET.get("qtd_votos","")
    if query_votos == "": query_votos = "30000"
    filtros['votos'] = query_votos
    query_vivo = request.GET.get("vivo","")
    if query_vivo == "1":
        filtros["vivo"] = "checked"
        query_vivo = ("AND morte is NULL ")
    query_rank = request.GET.get("ordem","")
    if query_rank == "media" or query_rank == "":
        rankear = ("media")
        filtros['selected'] = "media"
    elif query_rank == "ponderada":
        rankear = ("ponderada")
        filtros['selected'] = "ponderada"
    elif query_rank == "qtd_top250":
        rankear = ("num_top250")
        filtros['selected'] = "qtd_top250"
    elif query_rank == "qtd_filmes":
        rankear = ("num_filmes")
        filtros['selected'] = "qtd_filmes"

    selecao =  (f"SELECT pessoa_id, nome, ROUND(nota_media, 1) as media, ROUND(nota_ponderada, 1) as ponderada, num_filmes, num_top250, url FROM (SELECT pessoa_id, nome, AVG(nota_media) AS nota_media, SUM(nota_media * num_votos) / SUM(num_votos) AS nota_ponderada, COUNT(DISTINCT filme_id) AS num_filmes, COUNT(nm) AS num_top250, url FROM pessoa NATURAL JOIN ator NATURAL JOIN foto NATURAL JOIN avaliacao NATURAL LEFT JOIN (SELECT filme_id, nota_media AS nm FROM TOP250) AS top250filmes WHERE num_votos > {query_votos} {query_vivo}GROUP BY nome) AS resultado WHERE num_filmes > {query_qtd_dirigidos} ORDER BY {rankear} DESC")

    cursor = connection.cursor()
    cursor.execute(selecao)
    diretores = dictfetchall(cursor)
    diretores = rank_dict(diretores)
    return render(request, "imdb_filmes/rank_ator.html",{
        "diretores": diretores,
        "filtros": filtros
    })

def rank_roterista(request):
    filtros = {}
    query_qtd_dirigidos = request.GET.get("qtd_dirigidos","")
    if query_qtd_dirigidos == "": query_qtd_dirigidos = "2"
    filtros['qtd_dirigidos'] = query_qtd_dirigidos
    query_votos = request.GET.get("qtd_votos","")
    if query_votos == "": query_votos = "30000"
    filtros['votos'] = query_votos
    query_vivo = request.GET.get("vivo","")
    if query_vivo == "1":
        filtros["vivo"] = "checked"
        query_vivo = ("AND morte is NULL ")
    query_rank = request.GET.get("ordem","")
    if query_rank == "media" or query_rank == "":
        rankear = ("media")
        filtros['selected'] = "media"
    elif query_rank == "ponderada":
        rankear = ("ponderada")
        filtros['selected'] = "ponderada"
    elif query_rank == "qtd_top250":
        rankear = ("num_top250")
        filtros['selected'] = "qtd_top250"
    elif query_rank == "qtd_filmes":
        rankear = ("num_filmes")
        filtros['selected'] = "qtd_filmes"

    selecao =  (f"SELECT pessoa_id, nome, ROUND(nota_media, 1) as media, ROUND(nota_ponderada, 1) as ponderada, num_filmes, num_top250, url FROM (SELECT pessoa_id, nome, AVG(nota_media) AS nota_media, SUM(nota_media * num_votos) / SUM(num_votos) AS nota_ponderada, COUNT(DISTINCT filme_id) AS num_filmes, COUNT(nm) AS num_top250, url FROM pessoa NATURAL JOIN roterista NATURAL JOIN foto NATURAL JOIN avaliacao NATURAL LEFT JOIN (SELECT filme_id, nota_media AS nm FROM TOP250) AS top250filmes WHERE num_votos > {query_votos} {query_vivo}GROUP BY nome) AS resultado WHERE num_filmes > {query_qtd_dirigidos} ORDER BY {rankear} DESC")

    cursor = connection.cursor()
    cursor.execute(selecao)
    diretores = dictfetchall(cursor)
    diretores = rank_dict(diretores)
    return render(request, "imdb_filmes/rank_roteirista.html",{
        "diretores": diretores,
        "filtros": filtros
    })

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
    cursor.execute(f"SELECT url FROM capa WHERE filme_id='{filme_id}'")
    capa = dictfetchall(cursor)
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
    cursor.execute(f"SELECT url from foto WHERE pessoa_id='{pessoa_id}'")
    foto = dictfetchall(cursor)
    return render(request, "imdb_filmes/pessoa.html", {
        "pessoa": pessoa,
        "foto": foto
    } )

def pesquisa(request):
        query = request.GET.get("q", "")
        cursor = connection.cursor()
        cursor.execute(f"SELECT distinct pessoa.pessoa_id, nome, url from pessoa, foto WHERE pessoa.pessoa_id=foto.pessoa_id AND MATCH (nome) AGAINST ('{query}')")
        pessoas = dictfetchall(cursor)
        cursor.execute(f"SELECT distinct f.filme_id, f.titulo_primario, lancamento, url from titulo as t, filme as f, capa as c WHERE t.filme_id=f.filme_id AND f.filme_id=c.filme_id AND MATCH (titulo) AGAINST ('{query}')")
        filmes = dictfetchall(cursor)
        return render(request, "imdb_filmes/pesquisa.html", {
        "pessoas": pessoas,
        "filmes": filmes
    } )