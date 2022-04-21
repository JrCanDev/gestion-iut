from django import forms
from management.models import Semestre, TPPromotion, TDPromotion

"""
def get_object_attrs(obj):
  try:
    return obj.__dict__
  except AttributeError:
    return {attr: getattr(obj, attr) for attr in obj.__slots__}
"""

class CourAdminForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(CourAdminForm, self).__init__(*args, **kwargs)
    if(self.instance.id):
      self.fields['semestre'].queryset = Semestre.objects.filter(annee=self.instance.module.promotion.annee)
      self.fields['tp_promotion'].queryset = TPPromotion.objects.all().filter(td_promotion__promotion=self.instance.module.promotion)
