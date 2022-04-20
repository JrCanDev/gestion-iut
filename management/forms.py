from django import forms
from management.models import TPPromotion


class TPPromotionListForm(forms.ModelForm):
  tp_promotion = forms.ModelMultipleChoiceField(queryset=TPPromotion.objects.all(), required=False)