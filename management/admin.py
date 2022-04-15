from django.contrib import admin
# Register your models here.
from django import forms

from management.models import Annee, Semestre, Promotion, TDPromotion, TPPromotion, Semaine, Professeur, Module, Cours

class SemestreInline(admin.TabularInline):
  model = Semestre
  extra = 1
class AnneeAdmin(admin.ModelAdmin):
  inlines = [SemestreInline]
admin.site.register(Annee, AnneeAdmin)


class SemaineInline(admin.TabularInline):
  model = Semaine
  extra = 1
class SemestreAdmin(admin.ModelAdmin):
  list_display = ('nom_semestre', 'annee')
  inlines = [SemaineInline]
admin.site.register(Semestre, SemestreAdmin)


class TDPromotionInline(admin.TabularInline):
  model = TDPromotion
  extra = 1
class PromotionAdmin(admin.ModelAdmin):
  list_display = ('nom_promotion', 'annee')
  inlines = [TDPromotionInline]
admin.site.register(Promotion, PromotionAdmin)

class TPPromotionInline(admin.TabularInline):
  model = TPPromotion
  fieldsets = ((None, {
    'fields': ('nom_tp_promotion',)
  }), )
  extra = 1
class TDPromotionAdmin(admin.ModelAdmin):
  list_display = ('nom_td_promotion', 'promotion', 'annee')
  inlines = [TPPromotionInline]

  def annee(self, obj):
    return obj.promotion.annee
admin.site.register(TDPromotion, TDPromotionAdmin)


admin.site.register(Professeur)

class CoursInline(admin.TabularInline):
  model = Cours
  extra = 1
class ModuleAdmin(admin.ModelAdmin):
  inlines = [CoursInline]
admin.site.register(Module, ModuleAdmin)

"""
class ProductAdminForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(ProductAdminForm, self).__init__(*args, **kwargs)
    #print(self.fields['tp_promotion'].__dict__)
    print(self.fields['tp_promotion']._queryset[0])
    #self.fields['tags'].label = 'Custom Label'

class SemaineToTDPromotionAdmin(admin.ModelAdmin):
  form = ProductAdminForm
  list_display = ('semaine', 'semestre', 'annee', 'tp_promotion', 'promotion')
  fieldsets = ((None, {
    'fields': ('semaine', 'tp_promotion')
  }), )

  def semestre(self, obj):
    return obj.semaine.semestre
  
  def annee(self, obj):
    return obj.semaine.semestre.annee

  def promotion(self, obj):
    return obj.tp_promotion.td_promotion.promotion

admin.site.register(SemaineToTDPromotion, SemaineToTDPromotionAdmin)
"""


"""
from management.models import Enseignements, Niveaux, Periodes, Professeurs, DetailService, Semestres, TypesEns, Ues, Unites, Modules
class DetailServiceInline(admin.TabularInline):
  model = DetailService
  extra = 1

class ProfesseursAdmin(admin.ModelAdmin):
  inlines = [DetailServiceInline]
admin.site.register(Professeurs, ProfesseursAdmin)


admin.site.register(DetailService)


admin.site.register(TypesEns)


class EnseignementsAdminInline(admin.TabularInline):
  model = Enseignements
  extra = 1

class UnitesAdmin(admin.ModelAdmin):
  inlines = [EnseignementsAdminInline]
admin.site.register(Unites, UnitesAdmin)


class SemestresInline(admin.TabularInline):
  model = Semestres
  extra = 1

class NiveauxAdmin(admin.ModelAdmin):
  inlines = [SemestresInline]
admin.site.register(Niveaux, NiveauxAdmin)


admin.site.register(Semestres)


class EnseignementsInline(admin.TabularInline):
  model = Enseignements
  extra = 1

class PeriodesAdmin(admin.ModelAdmin):
  inlines = [EnseignementsInline]
admin.site.register(Periodes, PeriodesAdmin)


admin.site.register(Enseignements)


admin.site.register(Ues)


admin.site.register(Modules)
"""
