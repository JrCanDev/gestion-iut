from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from management.forms import AddWeek, DeleteForm
from management.models import Semester, Week


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

            if len(Week.objects.filter(semester=semester_id, name_week=form.cleaned_data['name_week']).all()):
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
            Week(semester=semester, name_week=form.cleaned_data['name_week']).save()
            return HttpResponseRedirect(reverse('management:managed-semester', args=(year_id, semester_id)))
    else:
        '''
        Sinon on affiche le formulaire vide.
        '''

        form = AddWeek()
        return render(request, 'management/add-week.html',
                      {'form': form, 'year_id': year_id, 'semester_id': semester_id})


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
                      {'form': form, 'post_url': post_url, "back_url": back_url})
