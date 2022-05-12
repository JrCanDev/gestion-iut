from audioop import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from management.forms import AddCmSubject, AddTdSubject, AddTpSubject, DeleteForm
from management.models import Promotion, Sessions, Subject, Tp


@login_required
def addCmSession(request, promotion_id, subject_id):
  '''
  Affiche la vue responsable de l'ajout d'une séances (CM) pour une matière dans une promotion et gère le retour de celle-ci.
  '''
  post_url = reverse('management:add-cm-session', args=(promotion_id, subject_id))
  back_url = reverse('management:managed-subject', args=(promotion_id, subject_id))

  if request.method == 'POST':
    form = AddCmSubject(request.POST, promotion_id=promotion_id)
    if form.is_valid():
      '''
      Si le formulaire a été soumi, on vérifie que les champs ont été correctement remplis.
      '''

      subject = Subject.objects.get(pk=subject_id)
      promotion = Promotion.objects.get(pk=promotion_id)

      '''
      Calcule en fonction de la promotion le nombre de séances qui n'a pas encore été attribuée.
      '''

      nb_sessions_remaining = subject.number_cm_sessions

      for one_sessions in subject.sessions_set.all():
        if(one_sessions.type_sessions == "cm"):
          nb_sessions_remaining -= one_sessions.number_sessions
      
      if form.cleaned_data['number_sessions'] > nb_sessions_remaining:
        '''
        Si le nombre de séance attribuée et supérieure au nombre de séance restante alors on revoie le formulaire avec une erreur.
        '''

        return render(request, 'management/add-form.html', {'promotion_id': promotion_id, 'subject_id': subject_id, 'form': form, 'error': 'Vous ne pouvez pas affecter plus de ' + str(nb_sessions_remaining) + ' séances', 'post_url': post_url, "back_url": back_url})

      '''
      Ajoute les données à la BDD et redirige le client.
      '''

      new_session = Sessions(subject=subject, type_sessions='cm', teacher=form.cleaned_data['teacher'], number_sessions=form.cleaned_data['number_sessions'], promotion=promotion)
      new_session.save()
      return HttpResponseRedirect(reverse('management:managed-subject', args=(promotion_id, subject_id)))
  else:
    '''
    Sinon on affiche le formulaire vide.
    '''

    form = AddCmSubject(promotion_id=promotion_id)
    return render(request, 'management/add-form.html', {'promotion_id': promotion_id, 'subject_id': subject_id, 'form': form, 'post_url': post_url, "back_url": back_url})

@login_required
def addTdSession(request, promotion_id, subject_id):
  '''
  Affiche la vue responsable de l'ajout d'une séances (TD) pour une matière dans une promotion et gère le retour de celle-ci.
  '''
  post_url = reverse('management:add-td-session', args=(promotion_id, subject_id))
  back_url = reverse('management:managed-subject', args=(promotion_id, subject_id))

  if request.method == 'POST':
    form = AddTdSubject(request.POST, promotion_id=promotion_id)
    if form.is_valid():
      '''
      Si le formulaire a été soumi, on vérifie que les champs ont été correctement remplis.
      '''

      subject = Subject.objects.get(pk=subject_id)
      promotion = Promotion.objects.get(pk=promotion_id)

      '''
      Calcule en fonction du TD choisi le nombre de séances qui n'a pas encore été attribuée.
      '''

      nb_sessions_remaining = subject.number_td_sessions

      for one_sessions in subject.sessions_set.filter(td=form.cleaned_data['td']).all():
        if(one_sessions.type_sessions == "td"):
          nb_sessions_remaining -= one_sessions.number_sessions
      
      if form.cleaned_data['number_sessions'] > nb_sessions_remaining:
        '''
        Si le nombre de séance attribuée et supérieure au nombre de séance restante alors on revoie le formulaire avec une erreur.
        '''

        return render(request, 'management/add-form.html', {'promotion_id': promotion_id, 'subject_id': subject_id, 'form': form, 'error': 'Vous ne pouvez pas affecter plus de ' + str(nb_sessions_remaining) + ' séances', 'post_url': post_url, "back_url": back_url})

      '''
      Ajoute les données à la BDD et redirige le client.
      '''

      new_session = Sessions(subject=subject, type_sessions='td', promotion=promotion, teacher=form.cleaned_data['teacher'], number_sessions=form.cleaned_data['number_sessions'], td=form.cleaned_data['td'])
      new_session.save()
      return HttpResponseRedirect(reverse('management:managed-subject', args=(promotion_id, subject_id)))
  else:
    '''
    Sinon on affiche le formulaire vide.
    '''

    form = AddTdSubject(promotion_id=promotion_id)
    return render(request, 'management/add-form.html', {'promotion_id': promotion_id, 'subject_id': subject_id, 'form': form, 'post_url': post_url, "back_url": back_url})

@login_required
def addTpSession(request, promotion_id, subject_id):
  '''
  Affiche la vue responsable de l'ajout d'une séances (TP) pour une matière dans une promotion et gère le retour de celle-ci.
  '''
  post_url = reverse('management:add-tp-session', args=(promotion_id, subject_id))
  back_url = reverse('management:managed-subject', args=(promotion_id, subject_id))

  if request.method == 'POST':
    form = AddTpSubject(request.POST, promotion_id=promotion_id)
    if form.is_valid():
      '''
      Si le formulaire a été soumi, on vérifie que les champs ont été correctement remplis.
      '''

      subject = Subject.objects.get(pk=subject_id)
      promotion = Promotion.objects.get(pk=promotion_id)

      '''
      Calcule en fonction du TP choisi le nombre de séances qui n'a pas encore été attribuée.
      '''

      nb_sessions_remaining = subject.number_tp_sessions

      for one_sessions in subject.sessions_set.filter(tp=form.cleaned_data['tp']).all():
        if(one_sessions.type_sessions == "tp"):
          nb_sessions_remaining -= one_sessions.number_sessions
        
      if form.cleaned_data['number_sessions'] > nb_sessions_remaining:
        '''
        Si le nombre de séance attribuée et supérieure au nombre de séance restante alors on revoie le formulaire avec une erreur.
        '''

        return render(request, 'management/add-form.html', {'promotion_id': promotion_id, 'subject_id': subject_id, 'form': form, 'error': 'Vous ne pouvez pas affecter plus de ' + str(nb_sessions_remaining) + ' séances', 'post_url': post_url, "back_url": back_url})

      '''
      Ajoute les données à la BDD et redirige le client.
      '''

      new_session = Sessions(subject=subject, type_sessions='tp', promotion=promotion, teacher=form.cleaned_data['teacher'], number_sessions=form.cleaned_data['number_sessions'])
      tp = Tp.objects.get(pk=form.cleaned_data['tp'].id)
      new_session.save()
      new_session.tp.add(tp)
      new_session.save()
      return HttpResponseRedirect(reverse('management:managed-subject', args=(promotion_id, subject_id)))
  else:
    '''
    Sinon on affiche le formulaire vide.
    '''

    form = AddTpSubject(promotion_id=promotion_id)
    return render(request, 'management/add-form.html', {'promotion_id': promotion_id, 'subject_id': subject_id, 'form': form, 'post_url': post_url, "back_url": back_url})

@login_required
def deleteSession(request, promotion_id, subject_id, session_id):
  post_url = reverse('management:delete-session', args=(promotion_id, subject_id, session_id))
  back_url = reverse('management:managed-subject', args=(promotion_id, subject_id))

  if request.method == 'POST':
    form = DeleteForm(request.POST)
    if form.is_valid():
      if (not form.cleaned_data['confirm']):
        return render(request, 'management/delete-form.html', {'form': form, 'error': 'Vous devez confirmer la suppression', 'post_url': post_url, "back_url": back_url})
      
      session = Sessions.objects.get(pk=session_id)
      session.delete()
      return HttpResponseRedirect(reverse('management:managed-subject', args=(promotion_id, subject_id)))
  else:
    form = DeleteForm()
    return render(request, 'management/delete-form.html', {'form': form, 'post_url': post_url, "back_url": back_url})
