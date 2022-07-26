# imdb-with-filters
Trabalho de banco de dados. DCC UFRJ 2022.1

## Configurar banco de dados
> IMDb_completo.sql

no servidor mysql.
(está no drive)
https://we.tl/t-DvwE4Utp0K


## Configurar Django

Para baixar django:
> pip install Django

É necessário também

> pip install mysqlclient

Va no arquivo imdb/settings.py
em
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'imdb',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
Configura para o seu banco de dados.

No terminal na pasta ../imdb-django/
execute: 
> python manage.py makemigrations

> python manage.py migrate

Para executar o projeto

> python manage.py runserver

Starting development server at http... 

Pare ir para o index:
http://127.0.0.1:8000/imdb_filmes
