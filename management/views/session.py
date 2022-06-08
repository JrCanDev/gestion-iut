from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from management.forms import AddCmSubject, AddTdSubject, AddTpSubject, DeleteForm, EditSession
from management.models import Promotion, Sessions, Subject, Tp


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_cm_session(request, promotion_id, subject_id):
    """
    Affiche la vue responsable de l'ajout d'une séances (CM) pour une matière dans une promotion et gère le retour de
    celle-ci.
    """
    post_url = reverse('management:add-cm-session', args=(promotion_id, subject_id))
    back_url = reverse('management:managed-subject', args=(promotion_id, subject_id))

    subject = Subject.objects.get(pk=subject_id)
    promotion = Promotion.objects.get(pk=promotion_id)

    '''
    Calcule en fonction de la promotion le nombre de séances qui n'a pas encore été attribuée.
    '''

    nb_hours_remaining = subject.number_cm_sessions

    for one_sessions in subject.sessions_set.all():
        if one_sessions.type_sessions == "cm":
            nb_hours_remaining -= one_sessions.number_hours

    if request.method == 'POST':
        form = AddCmSubject(request.POST, promotion_id=promotion_id, nb_hours_remaining=nb_hours_remaining)
        if form.is_valid():
            '''
            Si le formulaire a été soumi, on vérifie que les champs ont été correctement remplis.
            '''

            '''
            if form.cleaned_data['number_hours'] > nb_hours_remaining:
                return render(request, 'management/add-form.html',
                              {'promotion_id': promotion_id, 'subject_id': subject_id, 'form': form,
                               'error': 'Vous ne pouvez pas affecter plus de ' + str(
                                   nb_hours_remaining) + ' séances', 'post_url': post_url, "back_url": back_url})
            '''

            '''
            Ajoute les données à la BDD et redirige le client.
            '''

            new_session = Sessions(subject=subject, type_sessions='cm', teacher=form.cleaned_data['teacher'],
                                   number_hours=form.cleaned_data['number_hours'], promotion=promotion)
            new_session.save()
            return HttpResponseRedirect(reverse('management:managed-subject', args=(promotion_id, subject_id)))
    else:
        '''
        Sinon on affiche le formulaire vide.
        '''

        form = AddCmSubject(promotion_id=promotion_id, nb_hours_remaining=nb_hours_remaining)
        return render(request, 'management/add-form.html',
                      {'promotion_id': promotion_id, 'subject_id': subject_id, 'form': form, 'post_url': post_url,
                       "back_url": back_url})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_td_session(request, promotion_id, subject_id):
    """
    Affiche la vue responsable de l'ajout d'une séances (TD) pour une matière dans une promotion et gère le retour de
    celle-ci.
    """
    post_url = reverse('management:add-td-session', args=(promotion_id, subject_id))
    back_url = reverse('management:managed-subject', args=(promotion_id, subject_id))

    subject = Subject.objects.get(pk=subject_id)
    promotion = Promotion.objects.get(pk=promotion_id)

    if request.method == 'POST':
        form = AddTdSubject(request.POST, subject=subject, nb_hours_remaining=subject.number_td_sessions)
        if form.is_valid():
            '''
            Si le formulaire a été soumi, on vérifie que les champs ont été correctement remplis.
            '''

            '''
            Calcule en fonction du TD choisi le nombre de séances qui n'a pas encore été attribuée.
            '''

            nb_hours_remaining = subject.number_td_sessions

            for one_sessions in subject.sessions_set.filter(td=form.cleaned_data['td']).all():
                if one_sessions.type_sessions == "td":
                    nb_hours_remaining -= one_sessions.number_hours

            '''
            if form.cleaned_data['number_hours'] > nb_hours_remaining:
                return render(request, 'management/add-form.html',
                              {'promotion_id': promotion_id, 'subject_id': subject_id, 'form': form,
                               'error': 'Vous ne pouvez pas affecter plus de ' + str(
                                   nb_hours_remaining) + ' séances', 'post_url': post_url, "back_url": back_url})
            '''

            '''
            Ajoute les données à la BDD et redirige le client.
            '''

            new_session = Sessions(subject=subject, type_sessions='td', promotion=promotion,
                                   teacher=form.cleaned_data['teacher'],
                                   number_hours=form.cleaned_data['number_hours'], td=form.cleaned_data['td'])
            new_session.save()
            return HttpResponseRedirect(reverse('management:managed-subject', args=(promotion_id, subject_id)))
    else:
        '''
        Sinon on affiche le formulaire vide.
        '''

        form = AddTdSubject(subject=subject, nb_hours_remaining=subject.number_td_sessions)
        return render(request, 'management/add-form.html',
                      {'promotion_id': promotion_id, 'subject_id': subject_id, 'form': form, 'post_url': post_url,
                       "back_url": back_url})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_tp_session(request, promotion_id, subject_id):
    """
    Affiche la vue responsable de l'ajout d'une séances (TP) pour une matière dans une promotion et gère le retour de
    celle-ci.
    """
    post_url = reverse('management:add-tp-session', args=(promotion_id, subject_id))
    back_url = reverse('management:managed-subject', args=(promotion_id, subject_id))

    subject = Subject.objects.get(pk=subject_id)
    promotion = Promotion.objects.get(pk=promotion_id)

    if request.method == 'POST':
        form = AddTpSubject(request.POST, subject=subject, nb_hours_remaining=subject.number_tp_sessions)
        if form.is_valid():
            '''
            Si le formulaire a été soumi, on vérifie que les champs ont été correctement remplis.
            '''

            '''
            Calcule en fonction du TP choisi le nombre de séances qui n'a pas encore été attribuée.
            '''

            nb_hours_remaining = subject.number_tp_sessions

            for one_sessions in subject.sessions_set.filter(tp=form.cleaned_data['tp']).all():
                if one_sessions.type_sessions == "tp":
                    nb_hours_remaining -= one_sessions.number_hours

            '''
            if form.cleaned_data['number_hours'] > nb_hours_remaining:
                return render(request, 'management/add-form.html',
                              {'promotion_id': promotion_id, 'subject_id': subject_id, 'form': form,
                               'error': 'Vous ne pouvez pas affecter plus de ' + str(
                                   nb_hours_remaining) + ' séances', 'post_url': post_url, "back_url": back_url})
            '''

            '''
            Ajoute les données à la BDD et redirige le client.
            '''

            new_session = Sessions(subject=subject, type_sessions='tp', promotion=promotion,
                                   teacher=form.cleaned_data['teacher'],
                                   number_hours=form.cleaned_data['number_hours'])
            tp = Tp.objects.get(pk=form.cleaned_data['tp'].id)
            new_session.save()
            new_session.tp.add(tp)
            new_session.save()
            return HttpResponseRedirect(reverse('management:managed-subject', args=(promotion_id, subject_id)))
    else:
        '''
        Sinon on affiche le formulaire vide.
        '''

        form = AddTpSubject(subject=subject, nb_hours_remaining=subject.number_tp_sessions)
        return render(request, 'management/add-form.html',
                      {'promotion_id': promotion_id, 'subject_id': subject_id, 'form': form, 'post_url': post_url,
                       "back_url": back_url})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_session(request, promotion_id, subject_id, session_id):
    post_url = reverse('management:delete-session', args=(promotion_id, subject_id, session_id))
    back_url = reverse('management:managed-subject', args=(promotion_id, subject_id))

    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data['confirm']:
                return render(request, 'management/delete-form.html',
                              {'form': form, 'error': 'Vous devez confirmer la suppression', 'post_url': post_url,
                               "back_url": back_url})

            session = Sessions.objects.get(pk=session_id)
            session.delete()
            return HttpResponseRedirect(reverse('management:managed-subject', args=(promotion_id, subject_id)))
    else:
        form = DeleteForm()
        return render(request, 'management/delete-form.html',
                      {'form': form, 'post_url': post_url, "back_url": back_url})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_session(request, promotion_id, subject_id, session_id):
    post_url = reverse('management:edit-session', args=(promotion_id, subject_id, session_id))
    back_url = reverse('management:managed-subject', args=(promotion_id, subject_id))

    session = Sessions.objects.get(pk=session_id)

    if request.method == 'POST':
        form = EditSession(request.POST, session=session)
        if form.is_valid():
            session.teacher = form.cleaned_data['teacher']
            session.number_hours = form.cleaned_data['number_hours']
            session.save()
            return HttpResponseRedirect(reverse('management:managed-subject', args=(promotion_id, subject_id)))
    else:
        form = EditSession(session=session)
        return render(request, 'management/edit-form.html',
                      {'form': form, 'post_url': post_url, "back_url": back_url})
