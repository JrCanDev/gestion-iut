from django.contrib import admin

from management.models import DetailService, Enseignements, Modules, Niveaux, Periodes, Professeurs, Semestres, Types_ens, Ues, Unites

# Register your models here.

class DetailServiceInline(admin.TabularInline):
  model = DetailService
  extra = 1

class ProfesseursAdmin(admin.ModelAdmin):
  inlines = [DetailServiceInline]
admin.site.register(Professeurs, ProfesseursAdmin)

class UnitesAdmin(admin.ModelAdmin):
  pass
admin.site.register(Unites, UnitesAdmin)

"""
class Types_ensAdmin(admin.ModelAdmin):
  pass
admin.site.register(Types_ens, Types_ensAdmin)

class DetailServiceAdmin(admin.ModelAdmin):
  pass
admin.site.register(DetailService, DetailServiceAdmin)

class TypesEnsAdmin(admin.ModelAdmin):
  pass
admin.site.register(TypesEns, TypesEnsAdmin)

class UnitesAdmin(admin.ModelAdmin):
  pass
admin.site.register(Unites, UnitesAdmin)

class NiveauxAdmin(admin.ModelAdmin):
  pass
admin.site.register(Niveaux, NiveauxAdmin)

class SemestresAdmin(admin.ModelAdmin):
  pass
admin.site.register(Semestres, SemestresAdmin)

class PeriodesAdmin(admin.ModelAdmin):
  pass
admin.site.register(Periodes, PeriodesAdmin)

class EnseignementsAdmin(admin.ModelAdmin):
  pass
admin.site.register(Enseignements, EnseignementsAdmin)

class UesAdmin(admin.ModelAdmin):
  pass
admin.site.register(Ues, UesAdmin)

class ModulesAdmin(admin.ModelAdmin):
  pass
admin.site.register(Modules, ModulesAdmin)
"""
