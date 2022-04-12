from django.contrib import admin
from management.models import Enseignements, Niveaux, Periodes, Professeurs, DetailService, Semestres, TypesEns, Ues, Unites, Modules

# Register your models here.
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
