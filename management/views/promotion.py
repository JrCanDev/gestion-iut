from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from management.forms import AddPromotion, DeleteForm
from management.models import Promotion


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_promotion(request):
    """
    Fiche la vue responsable de l'ajout d'une promotions et gère le retour de celle-ci.
    """
    post_url = reverse('management:add-promotion', args=())
    back_url = reverse('management:index', args=())

    if request.method == 'POST':
        form = AddPromotion(request.POST)
        if form.is_valid():
            '''
            Si le formulaire a été soumi, on vérifie que les champs ont été correctement remplis.
            '''

            if len(Promotion.objects.filter(name_promotion=form.cleaned_data['name_promotion']).all()):
                '''
                Si la promotions existe déjà on revoie le formulaire avec une erreur.
                '''

                return render(request, 'management/add-form.html',
                              {'form': form, 'error': 'La promotion existe déjà', 'post_url': post_url,
                               "back_url": back_url})

            '''
            Ajoute les données à la BDD et redirige le client.
            '''

            new_promotion = Promotion(name_promotion=form.cleaned_data['name_promotion'],
                                      year=form.cleaned_data['year'])
            new_promotion.save()
            return HttpResponseRedirect(reverse('management:managed-promotion', args=(new_promotion.id,)))
    else:
        '''
        Sinon on affiche le formulaire vide.
        '''

        form = AddPromotion()
        return render(request, 'management/add-form.html', {'form': form, 'post_url': post_url, "back_url": back_url})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def managed_promotion(request, promotion_id):
    """
    Affiche la vue qui rassemble toutes les données sur une promotion.
    """

    promotion = Promotion.objects.get(pk=promotion_id)
    td = promotion.td_set.all()
    subject = promotion.subject_set.all()
    return render(request, 'management/managed-promotion.html', {'promotion': promotion, 'td': td, 'subject': subject})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_promotion(request, promotion_id):
    post_url = reverse('management:delete-promotion', args=(promotion_id,))
    back_url = reverse('management:index', args=())

    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data['confirm']:
                return render(request, 'management/delete-form.html',
                              {'form': form, 'error': 'Vous devez confirmer la suppression', 'post_url': post_url,
                               "back_url": back_url})

            promotion = Promotion.objects.get(pk=promotion_id)
            promotion.delete()
            return HttpResponseRedirect(reverse('management:index', args=()))
    else:
        form = DeleteForm()
        return render(request, 'management/delete-form.html',
                      {'form': form, 'post_url': post_url, "back_url": back_url,
                       "info": "Tous les éléments liés à cette promotion seront aussi supprimés !"})
