import code
from tokenize import group
from django.db import models

# Create your models here.
class Professeurs(models.Model):
  code_prof = models.CharField(primary_key=True)
  nom_prof = models.CharField(max_length=50)

class DetailService(models.Model):
  code_prof = models.ForeignKey(Professeurs, on_delete=models.CASCADE)
  code_enseignement = models.IntegerField()
  type_ds = models.CharField(max_length=8)
  nombre = models.IntegerField()

  class Meta:
    unique_together = ('code_enseignement', 'type_ds')

class Types_ens(models.Manager):
  type_ens = models.CharField(primary_key=True)
  detail = models.CharField(max_length=50)
  coef_finan = models.FloatField()
  coef_temps = models.FloatField()

class Unites(models.Manager):
  code_unite = models.CharField(primary_key=True)
  libelle_unite = models.CharField(max_length=100)
  annee = models.DateField()

class Niveaux(models.Manager):
  code_niveau = models.CharField(primary_key=True)
  nom_niveau = models.CharField(max_length=80)

class Semestres(models.Manager):
  code_semestre = models.CharField(primary_key=True)
  nom_semestre = models.CharField(max_length=80)
  #code_niveau = models.ForeignKey(Niveaux, on_delete=models.CASCADE)
  groups_td = models.IntegerField()
  groups_tp = models.IntegerField()

class Periodes(models.Manager):
  code_periode = models.CharField(primary_key=True)
  nom_periodes = models.CharField(max_length=80)
  #code_semestre = models.ForeignKey(Semestres, on_delete=models.CASCADE)

class Enseignements(models.Manager):
  code_enseignement = models.ForeignKey(DetailService, on_delete=models.CASCADE)
  #code_unite = models.ForeignKey(Unites, on_delete=models.CASCADE)
  nb_semaines = models.FloatField()
  #code_periode = models.ForeignKey(Periodes, on_delete=models.CASCADE)
  n_cours = models.FloatField()
  n_td = models.FloatField()
  n_tp = models.FloatField()
  remarque = models.CharField(max_length=500)

class Ues(models.Manager):
  code_ue = models.CharField(primary_key=True)
  libelle_ue = models.CharField(max_length=80)
  coef_ue = models.DateField()
  code_semestre =  models.CharField(max_length=8)

class Modules(models.Manager):
  code_module = models.CharField(primary_key=True)
  libelle_module = models.CharField(max_length=80)
  coef_module = models.FloatField()
  #code_ue = models.ForeignKey(Ues, on_delete=models.CASCADE)
