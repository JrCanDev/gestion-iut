from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from management.forms import AddSemester, DeleteForm
from management.models import Semester, Year


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_semester(request, year_id):
    """
    Affiche la vue responsable de l'ajout d'un semestre et gère le retour de celle-ci.
    """
    post_url = reverse('management:add-semester', args=(year_id,))
    back_url = reverse('management:managed-year', args=(year_id,))

    if request.method == 'POST':
        form = AddSemester(request.POST)
        if form.is_valid():
            '''
            Si le formulaire a été soumi, on vérifie que les champs ont été correctement remplis.
            '''

            if len(Semester.objects.filter(year=year_id, name_semester=form.cleaned_data['name_semester']).all()):
                '''
                Si le semestre existe déjà on revoie le formulaire avec une erreur.
                '''

                return render(request, 'management/add-form.html',
                              {'form': form, 'error': 'Le semestre existe déjà', 'year_id': year_id,
                               "post_url": post_url, "back_url": back_url})

            '''
            Ajoute les données à la BDD et redirige le client.
            '''

            year = Year.objects.get(pk=year_id)
            Semester(year=year, name_semester=form.cleaned_data['name_semester']).save()
            return HttpResponseRedirect(reverse('management:managed-year', args=(year_id,)))
    else:
        '''
        Sinon on affiche le formulaire vide.
        '''

        form = AddSemester()
        return render(request, 'management/add-form.html',
                      {'form': form, 'year_id': year_id, 'post_url': post_url, "back_url": back_url})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def managed_semester(request, year_id, semester_id):
    year = Year.objects.get(pk=year_id)
    semester = Semester.objects.get(pk=semester_id)

    return render(request, 'management/managed-semester.html', {'year': year, 'semester': semester})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_semester(request, year_id, semester_id):
    post_url = reverse('management:delete-semester', args=(year_id, semester_id))
    back_url = reverse('management:managed-year', args=(year_id,))

    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data['confirm']:
                return render(request, 'management/delete-form.html',
                              {'form': form, 'error': 'Vous devez confirmer la suppression', 'post_url': post_url,
                               "back_url": back_url})

            semester = Semester.objects.get(pk=semester_id)
            semester.delete()
            return HttpResponseRedirect(reverse('management:managed-year', args=(year_id,)))
    else:
        form = DeleteForm()
        return render(request, 'management/delete-form.html',
                      {'form': form, 'post_url': post_url, "back_url": back_url,
                       "info": "Tous les éléments liés à ce semestre seront aussi supprimés !"})
