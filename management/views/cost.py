from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

from management.models import Sessions, Teacher, Subject, Semester, Year


@login_required
@user_passes_test(lambda u: u.is_superuser)
def managed_cost(request, year_id):
    teacher = Teacher.objects.all()
    year = Year.objects.get(pk=year_id)
    eq_td = {"cm": 1.5, "td": 1, "tp": 0.66}
    hour_price = 10.5

    cost_teacher = {}

    for one_teacher in teacher:
        cost_teacher[one_teacher.last_name] = {"cost": 0.0, "cm": 0.0, "td": 0.0, "tp": 0.0}

        for one_session in Sessions.objects.filter(teacher=one_teacher, promotion__year=year_id).all():
            cost_teacher[one_teacher.last_name][one_session.type_sessions] += float(one_session.number_hours)
            cost_teacher[one_teacher.last_name]["cost"] += float(
                (hour_price * eq_td[one_session.type_sessions]) * one_session.number_hours)

    cost_subject = {}

    for one_subject in Subject.objects.filter(promotion__year=year_id):
        cost_subject[one_subject.name_subject] = {"cost": 0.0, "cm": 0.0, "td": 0.0, "tp": 0.0}

        for one_session in Sessions.objects.filter(subject=one_subject).all():
            cost_subject[one_subject.name_subject][one_session.type_sessions] += float(one_session.number_hours)
            cost_subject[one_subject.name_subject]["cost"] += float(
                (hour_price * eq_td[one_session.type_sessions]) * one_session.number_hours)

    cost_semester = {}

    for one_semester in Semester.objects.filter(year=year_id):
        cost_semester[one_semester.name_semester] = {"cost": 0.0, "cm": 0.0, "td": 0.0, "tp": 0.0}

        for one_session in Sessions.objects.filter(subject__semester=one_semester).all():
            cost_semester[one_semester.name_semester][one_session.type_sessions] += float(one_session.number_hours)
            cost_semester[one_semester.name_semester]["cost"] += float(
                (hour_price * eq_td[one_session.type_sessions]) * one_session.number_hours)

    return render(request, 'management/cost.html',
                  {'year': year, "cost_teacher": cost_teacher, "cost_subject": cost_subject,
                   "cost_semester": cost_semester})
