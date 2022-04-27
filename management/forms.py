from django import forms

from management.models import Teacher, Year, Td, Tp

class AddYear(forms.Form):
  name_year = forms.CharField(max_length=20)

StatusChoices =(
  ("1", "professeur"),
  ("2", "vacataire"),
)
  
class AddTeacher(forms.Form):
  lastname = forms.CharField(max_length=50)
  firstname = forms.CharField(max_length=50)
  status = forms.ChoiceField(choices=StatusChoices)

class AddPromotion(forms.Form):
  name_promotion = forms.CharField(max_length=20)
  year = forms.ModelChoiceField(queryset=Year.objects.all())

class AddTD(forms.Form):
  name_td = forms.CharField(max_length=5)

class AddTP(forms.Form):
  name_tp = forms.CharField(max_length=5)

class AddSubject(forms.Form):
  name_subject = forms.CharField(max_length=20)
  number_cm_sessions = forms.IntegerField(min_value=0, initial=0)
  number_td_sessions = forms.IntegerField(min_value=0, initial=0)
  number_tp_sessions = forms.IntegerField(min_value=0, initial=0)

class AddCmSubject(forms.Form):
  teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())
  number_sessions = forms.IntegerField(min_value=1, initial=1)

class AddTdSubject(forms.Form):
  teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())
  number_sessions = forms.IntegerField(min_value=1, initial=1)

  def __init__(self, *args, **kwargs):
    self.promotion_id = kwargs.pop("promotion_id")
    super(AddTdSubject, self).__init__(*args, **kwargs)
    self.fields['td'] = forms.ModelChoiceField(queryset=Td.objects.filter(promotion=self.promotion_id).all())

class AddTpSubject(forms.Form):
  teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())
  number_sessions = forms.IntegerField(min_value=1, initial=1)
  
  def __init__(self, *args, **kwargs):
    self.promotion_id = kwargs.pop("promotion_id")
    super(AddTpSubject, self).__init__(*args, **kwargs)
    self.fields['tp'] = forms.ModelChoiceField(queryset=Tp.objects.filter(td__in=Td.objects.filter(promotion=self.promotion_id).all()).all())