from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from management.forms import AddSubject, DeleteForm, EditSubject
from management.models import Promotion, Subject, Td, Tp, Sessions


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_subject(request, promotion_id):
    """
    Affiche la vue responsable de l'ajout d'une matiere dans une promotion et gère le retour de celle-ci.
    """
    post_url = reverse('management:add-subject', args=(promotion_id,))
    back_url = reverse('management:managed-promotion', args=(promotion_id,))

    promotion = Promotion.objects.get(pk=promotion_id)

    if request.method == 'POST':
        form = AddSubject(request.POST, promotion=promotion)
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
                                  description=form.cleaned_data['description'],
                                  number_cm_sessions=form.cleaned_data['number_cm_sessions'],
                                  number_td_sessions=form.cleaned_data['number_td_sessions'],
                                  number_tp_sessions=form.cleaned_data['number_tp_sessions'],
                                  semester=form.cleaned_data['semester'], promotion=promotion)
            new_subject.save()
            return HttpResponseRedirect(reverse('management:managed-promotion', args=(promotion_id,)))
    else:
        '''
        Sinon on affiche le formulaire vide.
        '''

        form = AddSubject(promotion=promotion)
        return render(request, 'management/add-form.html',
                      {'promotion_id': promotion_id, 'form': form, 'post_url': post_url, "back_url": back_url})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def managed_subject(request, promotion_id, subject_id):
    """
    Affiche la vue qui rassemble toutes les données sur une matiere.
    """

    subject = Subject.objects.get(pk=subject_id)
    sessions = Sessions.objects.filter(subject=subject).all()
    promotion = Promotion.objects.get(pk=promotion_id)
    tp = Tp.objects.filter(td__in=Td.objects.filter(promotion=promotion, semester=subject.semester))

    '''
    Récupére le nombre de séances prévu pour la matière.
    '''

    nb_sessions = {
        "cm": {"foreseen": subject.number_cm_sessions,
               "remaining": subject.number_cm_sessions, "sessions": {}},
        "td": {"foreseen": subject.number_td_sessions,
               "remaining":
                   subject.number_td_sessions * len(promotion.td_set.filter(semester=subject.semester).all()),
               "sessions": {}},
        "tp": {"foreseen": subject.number_tp_sessions,
               "remaining": (subject.number_tp_sessions * len(tp)), "sessions": {}}}

    '''
    Calcule en fonction de la promotion le nombre de séances qui n'a pas encore été attribuée.
    '''

    for one_sessions in subject.sessions_set.all():
        if one_sessions.type_sessions == "cm":
            nb_sessions["cm"]["remaining"] -= one_sessions.number_hours
        if one_sessions.type_sessions == "td":
            nb_sessions["td"]["remaining"] -= one_sessions.number_hours
        if one_sessions.type_sessions == "tp":
            nb_sessions["tp"]["remaining"] -= one_sessions.number_hours

    '''
    Récupére toutes les séances TD, TP attribuer à cette matière.
    '''

    nb_sessions["cm"]["sessions"] = subject.sessions_set.filter(type_sessions="cm")

    for one_td in promotion.td_set.filter(semester=subject.semester).all():
        allocate_hours = 0
        for one in sessions.filter(td=one_td).values("number_hours"):
            allocate_hours += one["number_hours"]

        nb_sessions["td"]["sessions"][one_td] = {"data": subject.sessions_set.filter(td=one_td).all(),
                                                 "allocate_hours": allocate_hours}

        for one_tp in one_td.tp_set.all():
            allocate_hours = 0
            for one in sessions.filter(tp=one_tp).values("number_hours"):
                allocate_hours += one["number_hours"]

            nb_sessions["tp"]["sessions"][one_tp] = {"data": subject.sessions_set.filter(tp=one_tp).all(),
                                                     "allocate_hours": allocate_hours}

    '''
    Affiche la vue.
    '''

    return render(request, 'management/managed-subject.html',
                  {'promotion': promotion, 'subject': subject, 'nb_sessions': nb_sessions})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_subject(request, promotion_id, subject_id):
    """
    Affiche la vue responsable de l'ajout d'une matiere dans une promotion et gère le retour de celle-ci.
    """
    post_url = reverse('management:edit-subject', args=(promotion_id, subject_id))
    back_url = reverse('management:managed-promotion', args=(promotion_id,))

    subject = Subject.objects.get(pk=subject_id)

    if request.method == 'POST':
        form = EditSubject(request.POST, subject=subject)
        if form.is_valid():
            '''
            Si le formulaire a été soumi, on vérifie que les champs ont été correctement remplis.
            '''

            '''
            Ajoute les données à la BDD et redirige le client.
            '''

            subject.name_subject = form.cleaned_data['name_subject']
            subject.description = form.cleaned_data['description']
            subject.number_cm_sessions = form.cleaned_data['number_cm_sessions']
            subject.number_td_sessions = form.cleaned_data['number_td_sessions']
            subject.number_tp_sessions = form.cleaned_data['number_tp_sessions']
            subject.save()
            return HttpResponseRedirect(reverse('management:managed-promotion', args=(promotion_id,)))
    else:
        '''
        Sinon on affiche le formulaire vide.
        '''

        form = EditSubject(subject=subject)
        return render(request, 'management/add-form.html',
                      {'promotion_id': promotion_id, 'form': form, 'post_url': post_url, "back_url": back_url})


@login_required
@user_passes_test(lambda u: u.is_superuser)
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
                      {'form': form, 'post_url': post_url, "back_url": back_url,
                       "info": "Tous les éléments liés à cette matiere seront aussi supprimés !"})
