from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from management.forms import AddTD, DeleteForm
from management.models import Promotion, Td


@login_required
def add_td(request, promotion_id):
    """
    Affiche la vue responsable de l'ajout d'un TD dans une promotion et gère le retour de celle-ci.
    """
    post_url = reverse('management:add-td', args=(promotion_id,))
    back_url = reverse('management:managed-promotion', args=(promotion_id,))

    promotion = Promotion.objects.get(pk=promotion_id)
    print(promotion.year.semester_set.all())

    if request.method == 'POST':
        form = AddTD(request.POST, promotion=promotion)
        if form.is_valid():
            '''
            Si le formulaire a été soumi, on vérifie que les champs ont été correctement remplis.
            '''

            if len(Td.objects.filter(name_td=form.cleaned_data['name_td'], semester=form.cleaned_data['semester'],
                                     promotion=promotion_id).all()):
                '''
                Si le TD existe déjà dans la promotion on revoie le formulaire avec une erreur.
                '''

                return render(request, 'management/add-form.html',
                              {'promotion_id': promotion_id, 'form': form, 'error': 'Le TD existe déjà',
                               'post_url': post_url, "back_url": back_url})

            '''
            Ajoute les données à la BDD et redirige le client.
            '''

            promotion = Promotion.objects.get(pk=promotion_id)
            new_td = Td(name_td=form.cleaned_data['name_td'], semester=form.cleaned_data['semester'],
                        promotion=promotion)
            new_td.save()
        return HttpResponseRedirect(reverse('management:managed-promotion', args=(promotion_id,)))
    else:
        '''
        Sinon on affiche le formulaire vide.
        '''

        form = AddTD(promotion=promotion)
        return render(request, 'management/add-form.html',
                      {'promotion_id': promotion_id, 'form': form, 'post_url': post_url, "back_url": back_url})


@login_required
def managed_td(request, promotion_id, td_id):
    """
    Affiche la vue qui rassemble toutes les données sur un TD d'une promotion.
    """

    promotion = Promotion.objects.get(pk=promotion_id)
    td = Td.objects.get(pk=td_id)

    return render(request, 'management/managed-td.html', {'promotion': promotion, 'td': td})


@login_required
def delete_td(request, promotion_id, td_id):
    post_url = reverse('management:delete-td', args=(promotion_id, td_id))
    back_url = reverse('management:managed-promotion', args=(promotion_id,))

    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data['confirm']:
                return render(request, 'management/delete-form.html',
                              {'form': form, 'error': 'Vous devez confirmer la suppression', 'post_url': post_url,
                               "back_url": back_url})

            td = Td.objects.get(pk=td_id)
            td.delete()
            return HttpResponseRedirect(reverse('management:managed-promotion', args=(promotion_id,)))
    else:
        form = DeleteForm()
        return render(request, 'management/delete-form.html',
                      {'form': form, 'post_url': post_url, "back_url": back_url,
                       "info": "Tous les éléments liés à ce TD seront aussi supprimés !"})
