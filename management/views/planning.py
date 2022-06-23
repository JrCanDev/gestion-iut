from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from management.forms import AddPlanning, DeleteForm, AddWeekPlanning
from management.models import Planning, Promotion, Sessions, Week, Year, Semester


@login_required
@user_passes_test(lambda u: u.is_superuser)
def managed_planning(request, year_id):
    sessions = Sessions.objects.filter(promotion__in=Promotion.objects.filter(year=year_id).all()).all()
    week = Week.objects.all()
    year = Year.objects.get(pk=year_id)
    planning = Planning.objects.all()

    remaining_session = {}

    for one_sessions in sessions:
        remaining_session[one_sessions.id] = {"name_subject": one_sessions.subject.name_subject,
                                              "promotion": one_sessions.promotion,
                                              "number_hours": one_sessions.number_hours,
                                              'type_sessions': one_sessions.type_sessions,
                                              'teacher': one_sessions.teacher}

    for one_planning in planning:
        if one_planning.sessions.id in remaining_session:
            remaining_session[one_planning.sessions.id]["number_hours"] -= one_planning.number_hours

    return render(request, 'management/managed-planning.html',
                  {'week': week, 'year': year, 'remaining_session': remaining_session})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_planning(request, year_id, sessions_id):
    post_url = reverse('management:add-planning', args=(year_id, sessions_id))
    back_url = reverse('management:managed-planning', args=(year_id,))

    if request.method == 'POST':
        form = AddPlanning(request.POST, year_id=year_id)
        if form.is_valid():
            remaining_session = Sessions.objects.get(pk=sessions_id).number_hours

            for one_planning in Planning.objects.filter(sessions=sessions_id):
                remaining_session -= one_planning.number_hours

            if form.cleaned_data['number_hours'] > remaining_session:
                return render(request, 'management/add-form.html', {'form': form,
                                                                    'error': 'Vous ne pouvez pas affecter plus de '
                                                                             + str(remaining_session) + ' séances',
                                                                    'post_url': post_url, "back_url": back_url})

            sessions = Sessions.objects.get(pk=sessions_id)
            Planning(sessions=sessions, week=form.cleaned_data['week'],
                     number_hours=form.cleaned_data['number_hours']).save()
            return HttpResponseRedirect(reverse('management:managed-planning', args=(year_id,)))
    else:
        form = AddPlanning(year_id=year_id)
        return render(request, 'management/add-form.html', {'form': form, 'post_url': post_url, "back_url": back_url})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_planning(request, year_id, planning_id):
    post_url = reverse('management:delete-planning', args=(year_id, planning_id))
    back_url = reverse('management:managed-planning', args=(year_id,))

    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data['confirm']:
                return render(request, 'management/delete-form.html',
                              {'form': form, 'error': 'Vous devez confirmer la suppression', 'post_url': post_url,
                               "back_url": back_url})

            planning = Planning.objects.get(pk=planning_id)
            planning.delete()
            return HttpResponseRedirect(reverse('management:managed-planning', args=(year_id,)))
    else:
        form = DeleteForm()
        return render(request, 'management/delete-form.html',
                      {'form': form, 'post_url': post_url, "back_url": back_url})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def managed_week_planning(request, year_id, semester_id, week_id):
    year = Year.objects.get(pk=year_id)
    week = Week.objects.get(pk=week_id)
    semester = Semester.objects.get(pk=semester_id)
    sessions = Sessions.objects.filter(subject__semester=semester_id).all()
    planning = Planning.objects.all()

    remaining_session = {}

    for one_sessions in sessions:
        remaining_session[one_sessions.id] = {"name_subject": one_sessions.subject.name_subject,
                                              "promotion": one_sessions.promotion,
                                              "number_hours": one_sessions.number_hours,
                                              'type_sessions': one_sessions.type_sessions,
                                              'teacher': one_sessions.teacher}

    for one_planning in planning:
        if one_planning.sessions.id in remaining_session:
            remaining_session[one_planning.sessions.id]["number_hours"] -= one_planning.number_hours

    return render(request, 'management/managed-week-planning.html',
                  {"week": week, "remaining_session": remaining_session, "semester": semester, "year": year})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_week_planning(request, year_id, semester_id, week_id, sessions_id):
    post_url = reverse('management:add-week-planning', args=(year_id, semester_id, week_id, sessions_id))
    back_url = reverse('management:managed-week-planning', args=(year_id, semester_id, week_id))

    if request.method == 'POST':
        form = AddWeekPlanning(request.POST)
        if form.is_valid():
            remaining_session = Sessions.objects.get(pk=sessions_id).number_hours

            for one_planning in Planning.objects.filter(sessions=sessions_id):
                remaining_session -= one_planning.number_hours

            if form.cleaned_data['number_hours'] > remaining_session:
                return render(request, 'management/add-form.html', {'form': form,
                                                                    'error': 'Vous ne pouvez pas affecter plus de '
                                                                             + str(remaining_session) + ' séances',
                                                                    'post_url': post_url, "back_url": back_url})

            sessions = Sessions.objects.get(pk=sessions_id)
            week = Week.objects.get(pk=week_id)
            Planning(sessions=sessions, week=week, number_hours=form.cleaned_data['number_hours']).save()
            return HttpResponseRedirect(
                reverse('management:managed-week-planning', args=(year_id, semester_id, week_id)))
    else:
        form = AddWeekPlanning()
        return render(request, 'management/add-form.html', {'form': form, 'post_url': post_url, "back_url": back_url})
