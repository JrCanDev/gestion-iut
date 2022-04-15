from datetime import date
from django.db import models
from django.contrib import admin

# Create your models here.

class Annee(models.Model):
  nom_annee = models.CharField(max_length=12)

  def __str__(self):
    return self.nom_annee

class Semestre(models.Model):
  nom_semestre = models.CharField(max_length=12)
  annee = models.ForeignKey(Annee, on_delete=models.CASCADE)

  def __str__(self):
    return self.nom_semestre

class Promotion(models.Model):
  nom_promotion = models.CharField(max_length=12)
  annee = models.ForeignKey(Annee, on_delete=models.CASCADE)

  def __str__(self):
    return self.nom_promotion

class TDPromotion(models.Model):
  nom_td_promotion = models.CharField(max_length=12)
  promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)

  def __str__(self):
    return self.nom_td_promotion

class TPPromotion(models.Model):
  nom_tp_promotion = models.CharField(max_length=12)
  td_promotion = models.ForeignKey(TDPromotion, on_delete=models.CASCADE)

  def __str__(self):
    return self.nom_tp_promotion + " | " + self.td_promotion.promotion.nom_promotion
class Semaine(models.Model):
  nom_semaine = models.CharField(max_length=50)
  semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
  #tp_promotion_list = models.ManyToManyField(TPPromotion, through='SemaineToTDPromotion')

  def __str__(self):
    return self.nom_semaine + " | " + self.semestre.nom_semestre + " | " + self.semestre.annee.nom_annee

class Professeur(models.Model):
  nom_professeur = models.CharField(max_length=50)
  prenom_professeur = models.CharField(max_length=50)

  def __str__(self):
    return self.nom_professeur

class Module(models.Model):
  nom_module = models.CharField(max_length=50)

  def __str__(self):
    return self.nom_module

class Cours(models.Model):
  TypeCours = models.TextChoices('type', 'CM TD TP')
  type_cours = models.CharField(blank=True, choices=TypeCours.choices, max_length=10)
  nb_heure = models.IntegerField(default=0)
  module = models.ForeignKey(Module, on_delete=models.CASCADE)
  professeur = models.ForeignKey(Professeur, on_delete=models.CASCADE)
  tp_promotion = models.ForeignKey(TPPromotion, on_delete=models.CASCADE)
  semaine = models.ForeignKey(Semaine, on_delete=models.CASCADE)


"""
class SemaineToTDPromotion(models.Model):
  tp_promotion = models.ForeignKey(TPPromotion, on_delete=models.CASCADE)
  semaine = models.ForeignKey(Semaine, on_delete=models.CASCADE)
"""


"""
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
"""
