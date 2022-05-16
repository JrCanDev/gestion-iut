from django import forms

from management.models import Semester, Teacher, Year, Td, Tp, Week


class AddYear(forms.Form):
    name_year = forms.CharField(max_length=20)


StatusChoices = (
    ("1", "professeur"),
    ("2", "vacataire"),
)


class AddTeacher(forms.Form):
    last_name = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    password = forms.CharField(max_length=250, widget=forms.PasswordInput)
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
    description = forms.CharField(max_length=120)
    number_cm_sessions = forms.FloatField(min_value=0, initial=0)
    number_td_sessions = forms.FloatField(min_value=0, initial=0)
    number_tp_sessions = forms.FloatField(min_value=0, initial=0)


class AddCmSubject(forms.Form):
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())

    def __init__(self, *args, **kwargs):
        self.promotion_id = kwargs.pop("promotion_id")
        self.nb_hours_remaining = kwargs.pop("nb_hours_remaining")
        super(AddCmSubject, self).__init__(*args, **kwargs)
        self.fields["number_hours"] = forms.FloatField(min_value=0.25, initial=self.nb_hours_remaining)


class AddTdSubject(forms.Form):
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())

    def __init__(self, *args, **kwargs):
        self.promotion_id = kwargs.pop("promotion_id")
        self.nb_hours_remaining = kwargs.pop("nb_hours_remaining")
        super(AddTdSubject, self).__init__(*args, **kwargs)
        self.fields['td'] = forms.ModelChoiceField(queryset=Td.objects.filter(promotion=self.promotion_id).all())
        self.fields["number_hours"] = forms.FloatField(min_value=0.25, initial=self.nb_hours_remaining)

        """promotion = Promotion.objects.get(pk=self.promotion_id) year = Year.objects.get(pk=promotion.year.id) 
        self.fields['week'] = forms.ModelChoiceField(queryset=Week.objects.filter(semester__in=year.semester_set.all(
        )).all()) """


class AddTpSubject(forms.Form):
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())

    def __init__(self, *args, **kwargs):
        self.promotion_id = kwargs.pop("promotion_id")
        self.nb_hours_remaining = kwargs.pop("nb_hours_remaining")
        super(AddTpSubject, self).__init__(*args, **kwargs)
        self.fields['tp'] = forms.ModelChoiceField(
            queryset=Tp.objects.filter(td__in=Td.objects.filter(promotion=self.promotion_id).all()).all())
        self.fields["number_hours"] = forms.FloatField(min_value=0.25, initial=self.nb_hours_remaining)

        """promotion = Promotion.objects.get(pk=self.promotion_id) year = Year.objects.get(pk=promotion.year.id) 
        self.fields['week'] = forms.ModelChoiceField(queryset=Week.objects.filter(semester__in=year.semester_set.all(
        )).all()) """


class AddSemester(forms.Form):
    name_semester = forms.CharField(max_length=20)


class AddWeek(forms.Form):
    # name_week = forms.DateField(widget=forms.SelectDateWidget)
    name_week = forms.DateField(input_formats=['%m/%d/%Y'])


class Login(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=250, widget=forms.PasswordInput)


class AddPlanning(forms.Form):
    number_hours = forms.FloatField(min_value=0.25, initial=1)

    def __init__(self, *args, **kwargs):
        self.year_id = kwargs.pop("year_id")
        super(AddPlanning, self).__init__(*args, **kwargs)
        self.fields['week'] = forms.ModelChoiceField(
            queryset=Week.objects.filter(semester__in=Semester.objects.filter(year=self.year_id).all()).all())


class DeleteForm(forms.Form):
    confirm = forms.BooleanField()
