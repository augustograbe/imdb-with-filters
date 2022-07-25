# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Ator(models.Model):
    filme = models.OneToOneField('Filme', models.DO_NOTHING, primary_key=True)
    pessoa = models.ForeignKey('Pessoa', models.DO_NOTHING)
    personagem = models.TextField()

    class Meta:
        managed = False
        db_table = 'ator'
        unique_together = (('filme', 'pessoa', 'personagem'),)

class Avaliacao(models.Model):
    filme = models.OneToOneField('Filme', models.DO_NOTHING, primary_key=True)
    nota_media = models.FloatField(blank=True, null=True)
    num_votos = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'avaliacao'


class ConhecidoPor(models.Model):
    pessoa = models.OneToOneField('Pessoa', models.DO_NOTHING, primary_key=True)
    filme = models.ForeignKey('Filme', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'conhecido_por'
        unique_together = (('pessoa', 'filme'),)


class Diretor(models.Model):
    filme = models.OneToOneField('Filme', models.DO_NOTHING, primary_key=True)
    pessoa = models.ForeignKey('Pessoa', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'diretor'
        unique_together = (('filme', 'pessoa'),)


class Elenco(models.Model):
    filme = models.OneToOneField('Filme', models.DO_NOTHING, primary_key=True)
    papel = models.IntegerField()
    pessoa = models.ForeignKey('Pessoa', models.DO_NOTHING)
    categoria = models.CharField(max_length=255, blank=True, null=True)
    trabalho = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'elenco'
        unique_together = (('filme', 'papel'),)


class Filme(models.Model):
    filme_id = models.CharField(primary_key=True, max_length=255)
    titulo_primario = models.TextField(blank=True, null=True)
    titulo_original = models.TextField(blank=True, null=True)
    lancamento = models.IntegerField(blank=True, null=True)
    tempo = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'filme'


class Genero(models.Model):
    filme = models.OneToOneField(Filme, models.DO_NOTHING, primary_key=True)
    genero = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'genero'
        unique_together = (('filme', 'genero'),)


class Pessoa(models.Model):
    pessoa_id = models.CharField(primary_key=True, max_length=255)
    nome = models.CharField(max_length=255)
    nascimento = models.SmallIntegerField(blank=True, null=True)
    morte = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pessoa'


class Roterista(models.Model):
    filme = models.OneToOneField(Filme, models.DO_NOTHING, primary_key=True)
    pessoa = models.ForeignKey(Pessoa, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'roterista'
        unique_together = (('filme', 'pessoa'),)


class Titulo(models.Model):
    filme = models.ForeignKey(Filme, models.DO_NOTHING)
    titulo = models.TextField()
    regiao = models.CharField(max_length=4, blank=True, null=True)
    lingua = models.CharField(max_length=4, blank=True, null=True)
    original = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'titulo'


class TrabalhouComo(models.Model):
    pessoa = models.OneToOneField(Pessoa, models.DO_NOTHING, primary_key=True)
    profissao = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'trabalhou_como'
        unique_together = (('pessoa', 'profissao'),)
