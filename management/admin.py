from django.contrib import admin
# Register your models here.
from django import forms
from management.forms import CourAdminForm
from management.models import Annee, Semestre, Promotion, TDPromotion, TPPromotion, Professeur, Module, Cour
from django.urls import reverse
class SemestreInline(admin.TabularInline):
  model = Semestre
  extra = 1
class AnneeAdmin(admin.ModelAdmin):
  inlines = [SemestreInline]
admin.site.register(Annee, AnneeAdmin)


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

"""
class TPPromotionList(ChangeList):
  def __init__(self, request, model, list_display, list_display_links, list_filter, date_hierarchy, search_fields, list_select_related, list_per_page, list_max_show_all, list_editable, model_admin):
    super(TPPromotionList, self).__init__(request, model, list_display, list_display_links, list_filter, date_hierarchy, search_fields, list_select_related,list_per_page, list_max_show_all, list_editable, model_admin)
    
    # these need to be defined here, and not in MovieAdmin
    self.list_display = ['action_checkbox', 'nom_tp_promotion', 'nom_tp_promotion']
    self.list_display_links = ['nom_tp_promotion']
    self.list_editable = ['nom_tp_promotion']
"""
def get_object_attrs(obj):
  try:
    return obj.__dict__
  except AttributeError:
    return {attr: getattr(obj, attr) for attr in obj.__slots__}


class CourInline(admin.TabularInline):
  model = Cour
  extra = 0
  readonly_fields = ("semestre", "tp_promotion",)
  #filter_horizontal = ("tp_promotion",)
  fieldsets = ((None, {'fields': ('type_cours', 'nb_heure', 'professeur', 'semestre', 'tp_promotion')}),)
  
  """
    def get_changelist(self, request, **kwargs):
      return TPPromotionList

    def get_changelist_form(self, request, **kwargs):
      return TPPromotionListForm
  """

class ModuleAdmin(admin.ModelAdmin):
  list_display = ('nom_module', 'promotion')
  inlines = [CourInline]

admin.site.register(Module, ModuleAdmin)


class CourAdmin(admin.ModelAdmin):
  fieldsets = ((None, {'fields': ('type_cours', 'module', 'nb_heure', 'semestre', 'professeur', 'tp_promotion')}),)
  filter_horizontal = ("tp_promotion",)
  form = CourAdminForm
  list_display = ('module', 'professeur', 'type_cours', 'promotion', 'semestre', 'annee')

  def annee(self, obj):
    return obj.module.promotion.annee
  
  def promotion(self, obj):
    return obj.module.promotion

  def has_add_permission(self, request, obj=None):
    return False
  """
  def render_change_form(self, request, context, *args, **kwargs):
    print(get_object_attrs(self.instance))

    context['adminform'].form.fields['semestre'].queryset = Semestre.objects.filter(annee='1')
    return super(CourAdmin, self).render_change_form(request, context, *args, **kwargs)
  """
admin.site.register(Cour, CourAdmin)

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
