from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from management.forms import AddSubject, DeleteForm
from management.models import Promotion, Subject


@login_required
def add_subject(request, promotion_id):
    """
    Affiche la vue responsable de l'ajout d'une matiere dans une promotion et gère le retour de celle-ci.
    """
    post_url = reverse('management:add-subject', args=(promotion_id,))
    back_url = reverse('management:managed-promotion', args=(promotion_id,))

    if request.method == 'POST':
        form = AddSubject(request.POST)
        if form.is_valid():
            '''
            Si le formulaire a été soumi, on vérifie que les champs ont été correctement remplis.
            '''

            if (
                    len(Subject.objects.filter(name_subject=form.cleaned_data['name_subject'],
                                               promotion=promotion_id).all())):
                '''
                Si la matiere existe déjà dans la promotion on revoie le formulaire avec une erreur.
                '''

                return render(request, 'management/add-form.html',
                              {'promotion_id': promotion_id, 'form': form, 'error': 'La matiere existe déjà',
                               'post_url': post_url, "back_url": back_url})

            '''
            Ajoute les données à la BDD et redirige le client.
            '''

            promotion = Promotion.objects.get(pk=promotion_id)
            new_subject = Subject(name_subject=form.cleaned_data['name_subject'],
                                  number_cm_sessions=form.cleaned_data['number_cm_sessions'],
                                  number_td_sessions=form.cleaned_data['number_td_sessions'],
                                  number_tp_sessions=form.cleaned_data['number_tp_sessions'], promotion=promotion)
            new_subject.save()
            return HttpResponseRedirect(reverse('management:managed-promotion', args=(promotion_id,)))
    else:
        '''
        Sinon on affiche le formulaire vide.
        '''

        form = AddSubject()
        return render(request, 'management/add-form.html',
                      {'promotion_id': promotion_id, 'form': form, 'post_url': post_url, "back_url": back_url})


@login_required
def managed_subject(request, promotion_id, subject_id):
    """
    Affiche la vue qui rassemble toutes les données sur une matiere.
    """

    subject = Subject.objects.get(pk=subject_id)
    promotion = Promotion.objects.get(pk=promotion_id)

    '''
    Récupére le nombre de séances prévu pour la matière.
    '''

    nb_sessions = {"cm": {"for_promotion": subject.number_cm_sessions, "remaining": subject.number_cm_sessions},
                   "td": {"for_td": subject.number_td_sessions,
                          "remaining": (subject.number_td_sessions * len(promotion.td_set.all()))},
                   "tp": {"for_tp": subject.number_tp_sessions, "remaining": 0}}

    for one_td in promotion.td_set.all():
        nb_sessions["tp"]["remaining"] += (subject.number_tp_sessions * len(one_td.tp_set.all()))

    '''
    Calcule en fonction de la promotion le nombre de séances qui n'a pas encore été attribuée.
    '''

    for one_sessions in subject.sessions_set.all():
        if one_sessions.type_sessions == "cm":
            nb_sessions["cm"]["remaining"] -= one_sessions.number_sessions
        if one_sessions.type_sessions == "td":
            nb_sessions["td"]["remaining"] -= one_sessions.number_sessions
        if one_sessions.type_sessions == "tp":
            nb_sessions["tp"]["remaining"] -= one_sessions.number_sessions

    '''
    Récupére toutes les séances TD, TP attribuer à cette matière.
    '''

    session_td = {}
    session_tp = {}

    for one_td in promotion.td_set.all():
        session_td[one_td] = (subject.sessions_set.filter(td=one_td).all())

        for one_tp in one_td.tp_set.all():
            session_tp[one_tp] = (subject.sessions_set.filter(tp=one_tp).all())

    '''
    Affiche la vue.
    '''

    return render(request, 'management/managed-subject.html',
                  {'promotion': promotion, 'subject': subject, 'nb_sessions': nb_sessions, "session_td": session_td,
                   "session_tp": session_tp})


@login_required
def delete_subject(request, promotion_id, subject_id):
    post_url = reverse('management:delete-subject', args=(promotion_id, subject_id))
    back_url = reverse('management:managed-promotion', args=(promotion_id,))

    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data['confirm']:
                return render(request, 'management/delete-form.html',
                              {'form': form, 'error': 'Vous devez confirmer la suppression', 'post_url': post_url,
                               "back_url": back_url})

            subject = Subject.objects.get(pk=subject_id)
            subject.delete()
            return HttpResponseRedirect(reverse('management:managed-promotion', args=(promotion_id,)))
    else:
        form = DeleteForm()
        return render(request, 'management/delete-form.html',
                      {'form': form, 'post_url': post_url, "back_url": back_url})
