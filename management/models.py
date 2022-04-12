from django.db import models

# Create your models here.
class Professeurs(models.Model):
  code_prof = models.CharField(primary_key=True, max_length=8)
  nom_prof = models.CharField(max_length=50)

class DetailService(models.Model):
  code_prof = models.ForeignKey(Professeurs, on_delete=models.CASCADE)
  type_ds = models.CharField(max_length=8)
  code_enseignement = models.IntegerField()
  nombre = models.IntegerField()

  class Meta:
    unique_together = ('code_enseignement', 'type_ds')

class TypesEns(models.Model):
  type_ens = models.CharField(primary_key=True, max_length=8)
  detail = models.CharField(max_length=50)
  coef_finan = models.FloatField()
  coef_temps = models.FloatField()

class Unites(models.Model):
  code_unite = models.CharField(primary_key=True, max_length=18)
  libelle_unite = models.CharField(max_length=100)
  annee = models.DateField()

class Niveaux(models.Model):
  code_niveau = models.CharField(primary_key=True, max_length=8)
  nom_niveau = models.CharField(max_length=80)

class Semestres(models.Model):
  code_semestre = models.CharField(primary_key=True, max_length=8)
  nom_semestre = models.CharField(max_length=80)
  code_niveau = models.ForeignKey(Niveaux, on_delete=models.CASCADE)
  groups_td = models.IntegerField()
  groups_tp = models.IntegerField()

class Periodes(models.Model):
  code_periode = models.CharField(primary_key=True, max_length=8)
  nom_periodes = models.CharField(max_length=80)
  code_semestre = models.ForeignKey(Semestres, on_delete=models.CASCADE)

class Enseignements(models.Model):
  code_enseignement = models.ForeignKey(DetailService, on_delete=models.CASCADE)
  code_unite = models.ForeignKey(Unites, on_delete=models.CASCADE)
  nb_semaines = models.FloatField()
  code_periode = models.ForeignKey(Periodes, on_delete=models.CASCADE)
  n_cours = models.FloatField()
  n_td = models.FloatField()
  n_tp = models.FloatField()
  remarque = models.CharField(max_length=500)

class Ues(models.Model):
  code_ue = models.CharField(primary_key=True, max_length=8)
  libelle_ue = models.CharField(max_length=80)
  coef_ue = models.DateField()
  code_semestre =  models.CharField(max_length=8)

class Modules(models.Model):
  code_module = models.CharField(primary_key=True, max_length=8)
  libelle_module = models.CharField(max_length=80)
  coef_module = models.FloatField()
  code_ue = models.ForeignKey(Ues, on_delete=models.CASCADE)
