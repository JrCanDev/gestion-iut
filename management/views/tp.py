from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from management.forms import AddTP, DeleteForm
from management.models import Td, Tp


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_tp(request, promotion_id, td_id):
    """
    Affiche la vue responsable de l'ajout d'un TP dans un TD d'une promotion et gère le retour de celle-ci.
    """
    post_url = reverse('management:add-tp', args=(promotion_id, td_id))
    back_url = reverse('management:managed-td', args=(promotion_id, td_id))

    if request.method == 'POST':
        form = AddTP(request.POST)
        if form.is_valid():
            '''
            Si le formulaire a été soumi, on vérifie que les champs ont été correctement remplis.
            '''

            list_tp = []
            td = Td.objects.get(pk=td_id)

            for one_td in Td.objects.filter(promotion=promotion_id, semester=td.semester.id).all():
                for one_tp in one_td.tp_set.all():
                    list_tp.append(one_tp.name_tp)

            if form.cleaned_data['name_tp'] in list_tp:
                '''
                Si le TP existe déjà dans la promotion on revoie le formulaire avec une erreur.
                '''

                return render(request, 'management/add-form.html',
                              {'promotion_id': promotion_id, 'td_id': td_id, 'form': form, 'error': 'Le TP existe déjà',
                               'post_url': post_url, "back_url": back_url})

            '''
            Ajoute les données à la BDD et redirige le client.
            '''

            td = Td.objects.get(pk=td_id)
            new_tp = Tp(name_tp=form.cleaned_data['name_tp'], td=td)
            new_tp.save()
        return HttpResponseRedirect(reverse('management:managed-td', args=(promotion_id, td_id)))
    else:
        '''
        Sinon on affiche le formulaire vide.
        '''

        form = AddTP()
        return render(request, 'management/add-form.html',
                      {'promotion_id': promotion_id, 'td_id': td_id, 'form': form, 'post_url': post_url,
                       "back_url": back_url})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_tp(request, promotion_id, td_id, tp_id):
    post_url = reverse('management:delete-tp', args=(promotion_id, td_id, tp_id))
    back_url = reverse('management:managed-td', args=(promotion_id, td_id))

    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data['confirm']:
                return render(request, 'management/delete-form.html',
                              {'form': form, 'error': 'Vous devez confirmer la suppression', 'post_url': post_url,
                               "back_url": back_url})

            tp = Tp.objects.get(pk=tp_id)
            tp.delete()
            return HttpResponseRedirect(reverse('management:managed-td', args=(promotion_id, td_id)))
    else:
        form = DeleteForm()
        return render(request, 'management/delete-form.html',
                      {'form': form, 'post_url': post_url, "back_url": back_url,
                       "info": "Tous les éléments liés à ce TP seront aussi supprimés !"})
