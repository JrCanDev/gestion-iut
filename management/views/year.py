from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from management.forms import AddYear, DeleteForm
from management.models import Year


@login_required
def add_year(request):
    """
    Affiche la vue responsable de l'ajout d'une année et gère le retour de celle-ci.
    """
    post_url = reverse('management:add-year', args=())
    back_url = reverse('management:index', args=())

    if request.method == 'POST':
        form = AddYear(request.POST)
        if form.is_valid():
            '''
            Si le formulaire a été soumi, on vérifie que les champs ont été correctement remplis.
            '''

            if len(Year.objects.filter(name_year=form.cleaned_data['name_year']).all()):
                '''
                Si l'année existe déjà on revoie le formulaire avec une erreur.
                '''

                return render(request, 'management/add-form.html',
                              {'form': form, 'error': 'L\'année existe déjà', post_url: post_url, "back_url": back_url})

            '''
            Ajoute les données à la BDD et redirige le client.
            '''

            Year(name_year=form.cleaned_data['name_year']).save()
            return HttpResponseRedirect('/')
    else:
        '''
        Sinon on affiche le formulaire vide.
        '''

        form = AddYear()
        return render(request, 'management/add-form.html', {'form': form, 'post_url': post_url, "back_url": back_url})


@login_required
def managed_year(request, year_id):
    """
    Affiche la vue qui rassemble toutes les données sur une année.
    """

    year = Year.objects.get(pk=year_id)

    return render(request, 'management/managed-year.html', {'year': year})


@login_required
def delete_year(request, year_id):
    post_url = reverse('management:delete-year', args=(year_id,))
    back_url = reverse('management:index', args=())

    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data['confirm']:
                return render(request, 'management/delete-form.html',
                              {'form': form, 'error': 'Vous devez confirmer la suppression', 'post_url': post_url,
                               "back_url": back_url})

            year = Year.objects.get(pk=year_id)
            year.delete()
            return HttpResponseRedirect(reverse('management:index', args=()))
    else:
        form = DeleteForm()
        return render(request, 'management/delete-form.html',
                      {'form': form, 'post_url': post_url, "back_url": back_url,
                       "info": "Tous les éléments liés à cette année seront aussi supprimés !"})
