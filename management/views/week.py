import datetime
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from management.forms import AddWeek, DeleteForm
from management.models import Week, Semester, Planning


def monday_of_week(year, num_week):
    """
    Calcul du premier et du dernier jour de la semaine ISO
    """
    d = date(year, 1, 1)
    delta_days = d.isoweekday() - 1
    delta_weeks = num_week
    if year == d.isocalendar()[0]:
        delta_weeks -= 1
    # delta for the beginning of the week
    delta = timedelta(days=-delta_days, weeks=delta_weeks)
    monday = d + delta
    return monday


def next_week(semester_id):
    semester = Semester.objects.get(pk=semester_id)
    weeks = Week.objects.filter(semester=semester).all()

    max_num_week = 0
    max_week_year = 0

    for one_week in weeks:
        week_date = str(one_week.name_week).split("-")
        num_week = datetime.date(int(week_date[0]), int(week_date[1]), int(week_date[2])).isocalendar()[1]
        if num_week > max_num_week:
            max_num_week = num_week
            max_week_year = int(week_date[0])

    name_week = monday_of_week(max_week_year, max_num_week + 1)
    return Week(semester=semester, name_week=name_week)


@login_required
def add_week(request, year_id, semester_id):
    """
    Affiche la vue responsable de l'ajout d'une semaine et gère le retour de celle-ci.
    """

    if request.method == 'POST':
        form = AddWeek(request.POST)
        if form.is_valid():
            '''
            Si le formulaire a été soumi, on vérifie que les champs ont été correctement remplis.
            '''

            date_select = str(form.cleaned_data['name_week']).split("-")
            num_week = datetime.date(int(date_select[0]), int(date_select[1]), int(date_select[2])).isocalendar()[1]
            name_week = monday_of_week(int(date_select[0]), num_week)

            if len(Week.objects.filter(semester=semester_id, name_week=name_week).all()):
                '''
                Si la semaine existe déjà on revoie le formulaire avec une erreur.
                '''

                return render(request, 'management/add-week.html',
                              {'form': form, 'error': 'La semaine existe déjà', 'year_id': year_id,
                               'semester_id': semester_id})

            '''
            Ajoute les données à la BDD et redirige le client.
            '''

            semester = Semester.objects.get(pk=semester_id)
            Week(semester=semester, name_week=name_week).save()
            return HttpResponseRedirect(reverse('management:managed-semester', args=(year_id, semester_id)))
    else:
        '''
        Sinon on affiche le formulaire vide.
        '''

        form = AddWeek()
        return render(request, 'management/add-week.html',
                      {'form': form, 'year_id': year_id, 'semester_id': semester_id})


@login_required
def add_next_week(request, year_id, semester_id):
    next_week(semester_id).save()

    return HttpResponseRedirect(reverse('management:managed-semester', args=(year_id, semester_id)))


@login_required
def duplicate_next_week(request, year_id, semester_id, week_id):
    week = next_week(semester_id)
    week.save()

    for one_planning in Planning.objects.filter(week=week_id).all():
        Planning(sessions=one_planning.sessions, number_hours=one_planning.number_hours, week=week).save()

    return HttpResponseRedirect(reverse('management:managed-semester', args=(year_id, semester_id)))


@login_required
def delete_week(request, year_id, semester_id, week_id):
    post_url = reverse('management:delete-week', args=(year_id, semester_id, week_id))
    back_url = reverse('management:managed-semester', args=(year_id, semester_id))

    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data['confirm']:
                return render(request, 'management/delete-form.html',
                              {'form': form, 'error': 'Vous devez confirmer la suppression', 'post_url': post_url,
                               "back_url": back_url})

            week = Week.objects.get(pk=week_id)
            week.delete()
            return HttpResponseRedirect(reverse('management:managed-semester', args=(year_id, semester_id)))
    else:
        form = DeleteForm()
        return render(request, 'management/delete-form.html',
                      {'form': form, 'post_url': post_url, "back_url": back_url,
                       "info": "Tous les éléments liés à cette semaine seront aussi supprimés !"})
