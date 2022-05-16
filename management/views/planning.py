from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from management.forms import AddPlanning, DeleteForm
from management.models import Planning, Promotion, Sessions, Week, Year


@login_required
def managed_planning(request, year_id):
    sessions = Sessions.objects.filter(promotion__in=Promotion.objects.filter(year=year_id).all()).all()
    week = Week.objects.all()
    year = Year.objects.get(pk=year_id)
    planning = Planning.objects.all()

    remaining_session = {}

    for one_sessions in sessions:
        remaining_session[one_sessions.id] = {"name_subject": one_sessions.subject.name_subject,
                                              "promotion": one_sessions.promotion,
                                              "number_sessions": one_sessions.number_sessions,
                                              'type_sessions': one_sessions.type_sessions,
                                              'teacher': one_sessions.teacher}

    for one_planning in planning:
        if one_planning.sessions.id in remaining_session:
            remaining_session[one_planning.sessions.id]["number_sessions"] -= one_planning.number_sessions

    return render(request, 'management/managed-planning.html',
                  {'week': week, 'year': year, 'remaining_session': remaining_session})


@login_required
def add_planning(request, year_id, sessions_id):
    post_url = reverse('management:add-planning', args=(year_id, sessions_id))
    back_url = reverse('management:managed-planning', args=(year_id,))

    if request.method == 'POST':
        form = AddPlanning(request.POST, year_id=year_id)
        if form.is_valid():
            remaining_session = Sessions.objects.get(pk=sessions_id).number_sessions

            for one_planning in Planning.objects.filter(sessions=sessions_id):
                remaining_session -= one_planning.number_sessions

            if form.cleaned_data['number_sessions'] > remaining_session:
                return render(request, 'management/add-form.html', {'form': form,
                                                                    'error': 'Vous ne pouvez pas affecter plus de '
                                                                             + str(remaining_session) + ' séances',
                                                                    'post_url': post_url, "back_url": back_url})

            sessions = Sessions.objects.get(pk=sessions_id)
            Planning(sessions=sessions, week=form.cleaned_data['week'],
                     number_sessions=form.cleaned_data['number_sessions']).save()
            return HttpResponseRedirect(reverse('management:managed-planning', args=(year_id,)))
    else:
        form = AddPlanning(year_id=year_id)
        return render(request, 'management/add-form.html', {'form': form, 'post_url': post_url, "back_url": back_url})


@login_required
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
