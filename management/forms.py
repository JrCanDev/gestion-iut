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
    admin = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(AddTeacher, self).__init__(*args, **kwargs)
        self.fields['last_name'].label = "Nom"
        self.fields['first_name'].label = "Prénom"
        self.fields['password'].label = "Mot de passe"
        self.fields['status'].label = "Statut"
        self.fields['admin'].label = "Super-utilisateur"


class AddPromotion(forms.Form):
    name_promotion = forms.CharField(max_length=20)
    year = forms.ModelChoiceField(queryset=Year.objects.all())

    def __init__(self, *args, **kwargs):
        super(AddPromotion, self).__init__(*args, **kwargs)
        self.fields['name_promotion'].label = "Nom de la promotion"
        self.fields['year'].label = "Année de la promotion"


class AddTD(forms.Form):
    name_td = forms.CharField(max_length=5)

    def __init__(self, *args, **kwargs):
        self.promotion = kwargs.pop("promotion")
        super(AddTD, self).__init__(*args, **kwargs)
        self.fields['semester'] = forms.ModelChoiceField(queryset=self.promotion.year.semester_set.all())
        self.fields['name_td'].label = "Nom du TD"
        self.fields['semester'].label = "Semestre"


class AddTP(forms.Form):
    name_tp = forms.CharField(max_length=5)

    def __init__(self, *args, **kwargs):
        super(AddTP, self).__init__(*args, **kwargs)
        self.fields['name_tp'].label = "Nom du TP"


class AddSubject(forms.Form):
    name_subject = forms.CharField(max_length=20)
    description = forms.CharField(max_length=120)
    number_cm_sessions = forms.FloatField(min_value=0, initial=0)
    number_td_sessions = forms.FloatField(min_value=0, initial=0)
    number_tp_sessions = forms.FloatField(min_value=0, initial=0)

    def __init__(self, *args, **kwargs):
        self.promotion = kwargs.pop("promotion")
        super(AddSubject, self).__init__(*args, **kwargs)
        self.fields['semester'] = forms.ModelChoiceField(queryset=self.promotion.year.semester_set.all())
        self.fields['name_subject'].label = "Nom de la ressource"
        self.fields['description'].label = "Description"
        self.fields['number_cm_sessions'].label = "Nombre d'heures en cm"
        self.fields['number_td_sessions'].label = "Nombre d'heures par groupe TD"
        self.fields['number_tp_sessions'].label = "Nombre d'heures par groupe TP"
        self.fields['semester'].label = "Semestre"


class AddCmSubject(forms.Form):
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())

    def __init__(self, *args, **kwargs):
        self.promotion_id = kwargs.pop("promotion_id")
        self.nb_hours_remaining = kwargs.pop("nb_hours_remaining")
        super(AddCmSubject, self).__init__(*args, **kwargs)
        self.fields["number_hours"] = forms.FloatField(min_value=0.25, initial=self.nb_hours_remaining)

        self.fields['teacher'].label = "Professeur"
        self.fields['number_hours'].label = "Nombre d'heures"


class AddTdSubject(forms.Form):
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())

    def __init__(self, *args, **kwargs):
        self.subject = kwargs.pop("subject")
        self.nb_hours_remaining = kwargs.pop("nb_hours_remaining")
        super(AddTdSubject, self).__init__(*args, **kwargs)
        self.fields['td'] = forms.ModelChoiceField(
            queryset=Td.objects.filter(promotion=self.subject.promotion.id, semester=self.subject.semester).all())
        self.fields["number_hours"] = forms.FloatField(min_value=0.25, initial=self.nb_hours_remaining)

        self.fields['teacher'].label = "Professeur"
        self.fields['td'].label = "Groupe TD"
        self.fields['number_hours'].label = "Nombre d'heures"
        """promotion = Promotion.objects.get(pk=self.promotion_id) year = Year.objects.get(pk=promotion.year.id) 
        self.fields['week'] = forms.ModelChoiceField(queryset=Week.objects.filter(semester__in=year.semester_set.all(
        )).all()) """


class AddTpSubject(forms.Form):
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())

    def __init__(self, *args, **kwargs):
        self.subject = kwargs.pop("subject")
        self.nb_hours_remaining = kwargs.pop("nb_hours_remaining")
        super(AddTpSubject, self).__init__(*args, **kwargs)
        self.fields['tp'] = forms.ModelChoiceField(
            queryset=Tp.objects.filter(td__in=Td.objects.filter(promotion=self.subject.promotion.id,
                                                                semester=self.subject.semester).all()).all())
        self.fields["number_hours"] = forms.FloatField(min_value=0.25, initial=self.nb_hours_remaining)

        self.fields['teacher'].label = "Professeur"
        self.fields['tp'].label = "Groupe TP"
        self.fields['number_hours'].label = "Nombre d'heures"
        """promotion = Promotion.objects.get(pk=self.promotion_id) year = Year.objects.get(pk=promotion.year.id) 
        self.fields['week'] = forms.ModelChoiceField(queryset=Week.objects.filter(semester__in=year.semester_set.all(
        )).all()) """


class AddSemester(forms.Form):
    name_semester = forms.CharField(max_length=20)

    def __init__(self, *args, **kwargs):
        super(AddSemester, self).__init__(*args, **kwargs)
        self.fields['name_semester'].label = "Nom du semestre"


class AddWeek(forms.Form):
    # name_week = forms.DateField(widget=forms.SelectDateWidget)
    name_week = forms.DateField(input_formats=['%m/%d/%Y'])

    def __init__(self, *args, **kwargs):
        super(AddWeek, self).__init__(*args, **kwargs)
        self.fields['name_week'].label = "Nom de la semaine"


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

        self.fields['number_hours'].label = "Nombre d'heures"
        self.fields['week'].label = "Nom de la semaine"


class DeleteForm(forms.Form):
    confirm = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super(DeleteForm, self).__init__(*args, **kwargs)
        self.fields['confirm'].label = "Je valide"


class ChangePassword(forms.Form):
    password = forms.CharField(max_length=250, widget=forms.PasswordInput)


class EditTeacher(forms.Form):
    def __init__(self, *args, **kwargs):
        self.teacher = kwargs.pop("teacher")
        super(EditTeacher, self).__init__(*args, **kwargs)
        self.fields['last_name'] = forms.CharField(max_length=50, initial=self.teacher.last_name)
        self.fields['first_name'] = forms.CharField(max_length=50, initial=self.teacher.first_name)
        self.fields['status'] = forms.ChoiceField(choices=StatusChoices,
                                                  initial=(1 if self.teacher.status == "professeur" else 2))
        self.fields['admin'] = forms.BooleanField(required=False, initial=self.teacher.is_superuser)

        self.fields['last_name'].label = "Nom"
        self.fields['first_name'].label = "Prénom"
        self.fields['status'].label = "Statut"
        self.fields['admin'].label = "Super-utilisateur"


class EditSubject(forms.Form):
    def __init__(self, *args, **kwargs):
        self.subject = kwargs.pop("subject")
        super(EditSubject, self).__init__(*args, **kwargs)
        self.fields['name_subject'] = forms.CharField(max_length=20, initial=self.subject.name_subject)
        self.fields['description'] = forms.CharField(max_length=120, initial=self.subject.description)
        self.fields['number_cm_sessions'] = forms.FloatField(min_value=0, initial=self.subject.number_cm_sessions)
        self.fields['number_td_sessions'] = forms.FloatField(min_value=0, initial=self.subject.number_td_sessions)
        self.fields['number_tp_sessions'] = forms.FloatField(min_value=0, initial=self.subject.number_tp_sessions)
        self.fields['semester'] = forms.ModelChoiceField(queryset=self.subject.promotion.year.semester_set.all(),
                                                         initial=self.subject.semester)

        self.fields['name_subject'].label = "Nom de la ressource"
        self.fields['description'].label = "Description"
        self.fields['number_cm_sessions'].label = "Nombre d'heures en cm"
        self.fields['number_td_sessions'].label = "Nombre d'heures par groupe TD"
        self.fields['number_tp_sessions'].label = "Nombre d'heures par groupe TP"
        self.fields['semester'].label = "Semestre"


class EditSession(forms.Form):
    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop("session")
        super(EditSession, self).__init__(*args, **kwargs)
        self.fields['teacher'] = forms.ModelChoiceField(queryset=Teacher.objects.all(), initial=self.session.teacher)
        self.fields["number_hours"] = forms.FloatField(min_value=0.25, initial=self.session.number_hours)

        self.fields['teacher'].label = "Professeur"
        self.fields['number_hours'].label = "Nombre d'heures"


class AddWeekPlanning(forms.Form):
    number_hours = forms.FloatField(min_value=0.25, initial=1)


class UploadFileForm(forms.Form):
    weeks = forms.FileField()
    teacher = forms.FileField()
    promotion = forms.FileField()
    subject = forms.FileField()
    sessions = forms.FileField()
    planning = forms.FileField()


class EditSettings(forms.Form):
    def __init__(self, *args, **kwargs):
        self.settings = kwargs.pop("settings")
        super(EditSettings, self).__init__(*args, **kwargs)
        self.fields['teacher_hour_price'] = forms.FloatField(initial=self.settings["professeur"]["hour_price"])
        self.fields['teacher_price_cm'] = forms.FloatField(initial=self.settings["professeur"]["eq_td"]["cm"])
        self.fields['teacher_price_td'] = forms.FloatField(initial=self.settings["professeur"]["eq_td"]["td"])
        self.fields['teacher_price_tp'] = forms.FloatField(initial=self.settings["professeur"]["eq_td"]["tp"])
        self.fields['contractor_hour_price'] = forms.FloatField(initial=self.settings["vacataire"]["hour_price"])
        self.fields['contractor_price_cm'] = forms.FloatField(initial=self.settings["vacataire"]["eq_td"]["cm"])
        self.fields['contractor_price_td'] = forms.FloatField(initial=self.settings["vacataire"]["eq_td"]["td"])
        self.fields['contractor_price_tp'] = forms.FloatField(initial=self.settings["vacataire"]["eq_td"]["tp"])

        self.fields['teacher_hour_price'].label = "Prix horaire professeur"
        self.fields['teacher_price_cm'].label = "Coefficient pour une heure de CM"
        self.fields['teacher_price_td'].label = "Coefficient pour une heure de TD"
        self.fields['teacher_price_tp'].label = "Coefficient pour une heure de TP"
        self.fields['contractor_hour_price'].label = "Prix horaire vacataire"
        self.fields['contractor_price_cm'].label = "Coefficient pour une heure de CM"
        self.fields['contractor_price_td'].label = "Coefficient pour une heure de TD"
        self.fields['contractor_price_tp'].label = "Coefficient pour une heure de TP"
