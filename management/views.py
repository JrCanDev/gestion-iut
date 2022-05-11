from calendar import week
from hashlib import new
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from management.forms import AddPromotion, AddTeacher, AddYear, AddTD, AddTP, AddSubject, AddCmSubject, AddTdSubject, AddTpSubject, AddSemester, AddWeek, Login, AddPlanning
from management.models import Promotion, Semester, Subject, Teacher, Year, Td, Tp, Sessions, Week, Planning
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

@login_required
def index(request):
  '''
  Récupère les années, les professeurs et les promotions pour les envoyer à la vue.
  '''

  year = Year.objects.all()
  teacher = Teacher.objects.all()
  promotion = Promotion.objects.all()
  
  return render(request, 'management/index.html', {'year': year, 'teacher': teacher, 'promotion': promotion})

@login_required
def addYear(request):
  '''
  Affiche la vue responsable de l'ajout d'une année et gère le retour de celle-ci.
  '''
  post_url = reverse('management:add-year', args=())
  back_url = reverse('management:index', args=())

  if request.method == 'POST':
    form = AddYear(request.POST)
    if form.is_valid():
      '''
      Si le formulaire a été soumi, on vérifie que les champs ont été correctement remplis.
      '''

      if (len(Year.objects.filter(name_year=form.cleaned_data['name_year']).all())):
        '''
        Si l'année existe déjà on revoie le formulaire avec une erreur.
        '''

        return render(request, 'management/add-form.html', {'form': form, 'error': 'L\'année existe déjà', post_url: post_url, "back_url": back_url})
      
      '''
      Ajoute les données à la BDD et redirige le client.
      '''
      
      Year(name_year = form.cleaned_data['name_year']).save()
      return HttpResponseRedirect('/')
  else:
    '''
    Sinon on affiche le formulaire vide.
    '''

    form = AddYear()
    return render(request, 'management/add-form.html', {'form': form, 'post_url': post_url, "back_url": back_url})

@login_required
def addTeacher(request):
  '''
  Affiche la vue responsable de l'ajout d'un professeur et gère le retour de celle-ci.
  '''
  post_url = reverse('management:add-teacher', args=())
  back_url = reverse('management:index', args=())

  if request.method == 'POST':
    form = AddTeacher(request.POST)
    if form.is_valid():
      '''
      Si le formulaire a été soumi, on vérifie que les champs ont été correctement remplis.
      '''

      if (len(Teacher.objects.filter(last_name=form.cleaned_data['last_name'], first_name=form.cleaned_data['first_name']).all())):
        '''
        Si le professeur existe déjà on revoie le formulaire avec une erreur.
        '''

        return render(request, 'management/add-form.html', {'form': form, 'error': 'Le professeur existe déjà', 'post_url': post_url, "back_url": back_url })
      
      StatusChoices = {
        "1": "professeur",
        "2": "vacataire"
      }

      '''
      Ajoute les données à la BDD et redirige le client.
      '''
      user = Teacher.objects.create_user(form.cleaned_data['last_name'], '', form.cleaned_data['password'])
      user.last_name = form.cleaned_data['last_name']
      user.first_name = form.cleaned_data['first_name']
      user.status = StatusChoices[form.cleaned_data['status']]
      user.save()
      return HttpResponseRedirect('/')
  else:
    '''
    Sinon on affiche le formulaire vide.
    '''

    form = AddTeacher()
    return render(request, 'management/add-form.html', {'form': form, 'post_url': post_url, "back_url": back_url})

@login_required
def addPromotion(request):
  '''
  Affiche la vue responsable de l'ajout d'une promotions et gère le retour de celle-ci.
  '''
  post_url = reverse('management:add-promotion', args=())
  back_url = reverse('management:index', args=())

  if request.method == 'POST':
    form = AddPromotion(request.POST)
    if form.is_valid():
      '''
      Si le formulaire a été soumi, on vérifie que les champs ont été correctement remplis.
      '''

      if (len(Promotion.objects.filter(name_promotion=form.cleaned_data['name_promotion']).all())):
        '''
        Si la promotions existe déjà on revoie le formulaire avec une erreur.
        '''

        return render(request, 'management/add-form.html', {'form': form, 'error': 'La promotion existe déjà', 'post_url': post_url, "back_url": back_url })
      
      '''
      Ajoute les données à la BDD et redirige le client.
      '''

      new_promotion = Promotion(name_promotion=form.cleaned_data['name_promotion'], year=form.cleaned_data['year'])
      new_promotion.save()
      return HttpResponseRedirect(reverse('management:edit-promotion', args=(new_promotion.id,)))
  else:
    '''
    Sinon on affiche le formulaire vide.
    '''

    form = AddPromotion()
    return render(request, 'management/add-form.html', {'form': form, 'post_url': post_url, "back_url": back_url})

@login_required
def editPromotion(request, promotion_id):
  '''
  Affiche la vue qui rassemble toutes les données sur une promotion.
  '''

  promotion = Promotion.objects.get(pk=promotion_id)
  td = promotion.td_set.all()
  subject = promotion.subject_set.all()
  return render(request, 'management/edit-promotion.html', {'promotion': promotion, 'td': td, 'subject': subject})

@login_required
def addTd(request, promotion_id):
  '''
  Affiche la vue responsable de l'ajout d'un TD dans une promotion et gère le retour de celle-ci.
  '''
  post_url = reverse('management:add-td', args=(promotion_id,))
  back_url = reverse('management:edit-promotion', args=(promotion_id,))

  if request.method == 'POST':
    form = AddTD(request.POST)
    if form.is_valid():
      '''
      Si le formulaire a été soumi, on vérifie que les champs ont été correctement remplis.
      '''

      if (len(Td.objects.filter(name_td=form.cleaned_data['name_td'], promotion=promotion_id).all())):
        '''
        Si le TD existe déjà dans la promotion on revoie le formulaire avec une erreur.
        '''

        return render(request, 'management/add-form.html', {'promotion_id': promotion_id, 'form': form, 'error': 'Le TD existe déjà', 'post_url': post_url, "back_url": back_url})

      '''
      Ajoute les données à la BDD et redirige le client.
      '''

      promotion = Promotion.objects.get(pk=promotion_id)
      new_td = Td(name_td=form.cleaned_data['name_td'], promotion=promotion)
      new_td.save()
    return HttpResponseRedirect(reverse('management:edit-promotion', args=(promotion_id,)))
  else:
    '''
    Sinon on affiche le formulaire vide.
    '''

    form = AddTD()
    return render(request, 'management/add-form.html', {'promotion_id': promotion_id, 'form': form, 'post_url': post_url, "back_url": back_url})

@login_required
def editTd(request, promotion_id, td_id):
  '''
  Affiche la vue qui rassemble toutes les données sur un TD d'une promotion.
  '''

  promotion = Promotion.objects.get(pk=promotion_id)
  td = Td.objects.get(pk=td_id)

  return render(request, 'management/edit-td.html', {'promotion': promotion, 'td': td})

@login_required
def addTp(request, promotion_id, td_id):
  '''
  Affiche la vue responsable de l'ajout d'un TP dans un TD d'une promotion et gère le retour de celle-ci.
  '''
  post_url = reverse('management:add-tp', args=(promotion_id, td_id))
  back_url = reverse('management:edit-td', args=(promotion_id, td_id))

  if request.method == 'POST':
    form = AddTP(request.POST)
    if form.is_valid():
      '''
      Si le formulaire a été soumi, on vérifie que les champs ont été correctement remplis.
      '''

      list_tp = []

      for one_td in Td.objects.filter(promotion=promotion_id).all():
        for one_tp in one_td.tp_set.all():
          list_tp.append(one_tp.name_tp)
      
      if form.cleaned_data['name_tp'] in list_tp:
        '''
        Si le TP existe déjà dans la promotion on revoie le formulaire avec une erreur.
        '''

        return render(request, 'management/add-form.html', {'promotion_id': promotion_id, 'td_id': td_id, 'form': form, 'error': 'Le TP existe déjà', 'post_url': post_url, "back_url": back_url})

      '''
      Ajoute les données à la BDD et redirige le client.
      '''
      
      td = Td.objects.get(pk=td_id)
      new_tp = Tp(name_tp=form.cleaned_data['name_tp'], td=td)
      new_tp.save()
    return HttpResponseRedirect(reverse('management:edit-td', args=(promotion_id, td_id)))
  else:
    '''
    Sinon on affiche le formulaire vide.
    '''

    form = AddTP()
    return render(request, 'management/add-form.html', {'promotion_id': promotion_id, 'td_id': td_id, 'form': form, 'post_url': post_url, "back_url": back_url})

@login_required
def editYear(request, year_id):
  '''
  Affiche la vue qui rassemble toutes les données sur une année.
  '''

  year = Year.objects.get(pk=year_id)

  return render(request, 'management/edit-year.html', {'year': year})

@login_required
def addSubject(request, promotion_id):
  '''
  Affiche la vue responsable de l'ajout d'une matiere dans une promotion et gère le retour de celle-ci.
  '''
  post_url = reverse('management:add-subject', args=(promotion_id,))
  back_url = reverse('management:edit-promotion', args=(promotion_id,))

  if request.method == 'POST':
    form = AddSubject(request.POST)
    if form.is_valid():
      '''
      Si le formulaire a été soumi, on vérifie que les champs ont été correctement remplis.
      '''

      if (len(Subject.objects.filter(name_subject=form.cleaned_data['name_subject'], promotion=promotion_id).all())):
        '''
        Si la matiere existe déjà dans la promotion on revoie le formulaire avec une erreur.
        '''

        return render(request, 'management/add-form.html', {'promotion_id': promotion_id, 'form': form, 'error': 'La matiere existe déjà', 'post_url': post_url, "back_url": back_url})

      '''
      Ajoute les données à la BDD et redirige le client.
      '''

      promotion = Promotion.objects.get(pk=promotion_id)
      new_subject = Subject(name_subject=form.cleaned_data['name_subject'], number_cm_sessions=form.cleaned_data['number_cm_sessions'],  number_td_sessions=form.cleaned_data['number_td_sessions'],  number_tp_sessions=form.cleaned_data['number_tp_sessions'], promotion=promotion)
      new_subject.save()
      return HttpResponseRedirect(reverse('management:edit-promotion', args=(promotion_id,)))
  else:
    '''
    Sinon on affiche le formulaire vide.
    '''

    form = AddSubject()
    return render(request, 'management/add-form.html', {'promotion_id': promotion_id, 'form': form, 'post_url': post_url, "back_url": back_url})

@login_required
def editSubject(request, promotion_id, subject_id):
  '''
  Affiche la vue qui rassemble toutes les données sur une matiere.
  '''

  subject = Subject.objects.get(pk=subject_id)
  promotion = Promotion.objects.get(pk=promotion_id)

  '''
  Récupére le nombre de séances prévu pour la matière.
  '''

  nb_sessions = {}

  nb_sessions["cm"] = {"for_promotion": subject.number_cm_sessions, "remaining": subject.number_cm_sessions}
  nb_sessions["td"] = {"for_td": subject.number_td_sessions, "remaining": (subject.number_td_sessions * len(promotion.td_set.all()))}
  nb_sessions["tp"] = {"for_tp": subject.number_tp_sessions, "remaining": 0}
  
  for one_td in promotion.td_set.all():
    nb_sessions["tp"]["remaining"] += (subject.number_tp_sessions * len(one_td.tp_set.all()))

  '''
  Calcule en fonction de la promotion le nombre de séances qui n'a pas encore été attribuée.
  '''

  for one_sessions in subject.sessions_set.all():
    if(one_sessions.type_sessions == "cm"):
      nb_sessions["cm"]["remaining"] -= one_sessions.number_sessions
    if(one_sessions.type_sessions == "td"):
      nb_sessions["td"]["remaining"] -= one_sessions.number_sessions
    if(one_sessions.type_sessions == "tp"):
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

  return render(request, 'management/edit-subject.html', {'promotion': promotion, 'subject': subject, 'nb_sessions': nb_sessions, "session_td": session_td, "session_tp": session_tp})

@login_required
def addCmSession(request, promotion_id, subject_id):
  '''
  Affiche la vue responsable de l'ajout d'une séances (CM) pour une matière dans une promotion et gère le retour de celle-ci.
  '''
  post_url = reverse('management:add-cm-session', args=(promotion_id, subject_id))
  back_url = reverse('management:edit-subject', args=(promotion_id, subject_id))

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
      return HttpResponseRedirect(reverse('management:edit-subject', args=(promotion_id, subject_id)))
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
  back_url = reverse('management:edit-subject', args=(promotion_id, subject_id))

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
      return HttpResponseRedirect(reverse('management:edit-subject', args=(promotion_id, subject_id)))
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
  back_url = reverse('management:edit-subject', args=(promotion_id, subject_id))

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
      return HttpResponseRedirect(reverse('management:edit-subject', args=(promotion_id, subject_id)))
  else:
    '''
    Sinon on affiche le formulaire vide.
    '''

    form = AddTpSubject(promotion_id=promotion_id)
    return render(request, 'management/add-form.html', {'promotion_id': promotion_id, 'subject_id': subject_id, 'form': form, 'post_url': post_url, "back_url": back_url})


@login_required
def addSemester(request, year_id):
  '''
  Affiche la vue responsable de l'ajout d'un semestre et gère le retour de celle-ci.
  '''
  post_url = reverse('management:add-semester', args=(year_id,))
  back_url = reverse('management:edit-year', args=(year_id,))

  if request.method == 'POST':
    form = AddSemester(request.POST)
    if form.is_valid():
      '''
      Si le formulaire a été soumi, on vérifie que les champs ont été correctement remplis.
      '''

      if (len(Semester.objects.filter(year=year_id, name_semester=form.cleaned_data['name_semester']).all())):
        '''
        Si le semestre existe déjà on revoie le formulaire avec une erreur.
        '''

        return render(request, 'management/add-form.html', {'form': form, 'error': 'Le semestre existe déjà', 'year_id': year_id, "post_url": post_url, "back_url": back_url })
      
      '''
      Ajoute les données à la BDD et redirige le client.
      '''

      year = Year.objects.get(pk=year_id)
      Semester(year=year, name_semester=form.cleaned_data['name_semester']).save()
      return HttpResponseRedirect(reverse('management:edit-year', args=(year_id,)))
  else:
    '''
    Sinon on affiche le formulaire vide.
    '''

    form = AddSemester()
    return render(request, 'management/add-form.html', {'form': form, 'year_id': year_id, 'post_url': post_url, "back_url": back_url})

@login_required
def editSemester(request, year_id, semester_id):
  year = Year.objects.get(pk=year_id)
  semester = Semester.objects.get(pk=semester_id)

  return render(request, 'management/edit-semester.html', {'year': year, 'semester': semester})

@login_required
def addWeek(request, year_id, semester_id):
  '''
  Affiche la vue responsable de l'ajout d'une semaine et gère le retour de celle-ci.
  '''

  if request.method == 'POST':
    form = AddWeek(request.POST)
    if form.is_valid():
      '''
      Si le formulaire a été soumi, on vérifie que les champs ont été correctement remplis.
      '''

      if (len(Week.objects.filter(semester=semester_id, name_week=form.cleaned_data['name_week']).all())):
        '''
        Si la semaine existe déjà on revoie le formulaire avec une erreur.
        '''

        return render(request, 'management/add-week.html', {'form': form, 'error': 'La semaine existe déjà', 'year_id': year_id, 'semester_id': semester_id })
      
      '''
      Ajoute les données à la BDD et redirige le client.
      '''

      semester = Semester.objects.get(pk=semester_id)
      Week(semester=semester, name_week=form.cleaned_data['name_week']).save()
      return HttpResponseRedirect(reverse('management:edit-semester', args=(year_id, semester_id)))
  else:
    '''
    Sinon on affiche le formulaire vide.
    '''

    form = AddWeek()
    return render(request, 'management/add-week.html', {'form': form, 'year_id': year_id, 'semester_id': semester_id})

@login_required
def editTeacher(request, teacher_id):
  teacher = Teacher.objects.get(pk=teacher_id)
  year = Year.objects.all()

  return render(request, 'management/edit-teacher.html', {'teacher': teacher, 'year': year})

def userLogin(request):
  if request.method == 'POST':
    form = Login(request.POST)
    if form.is_valid():
      user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
      if user is not None:
        login(request, user)
        return HttpResponseRedirect(request.GET['next'])
      else:
        return render(request, 'management/login.html', {'form': form, 'error': 'Utilisateur et/ou les mots de pass et incorrect', 'next_url': request.GET['next']})
  else:
    form = Login()
    return render(request, 'management/login.html', {'form': form, 'next_url': request.GET['next']})

@login_required
def editPlanning(request, year_id):
  sessions = Sessions.objects.all()
  week = Week.objects.all()
  year = Year.objects.get(pk=year_id)
  planning = Planning.objects.all()

  remaining_session = {}

  for one_sessions in sessions:
    remaining_session[one_sessions.id] = {"name_subject" : one_sessions.subject.name_subject, "promotion": one_sessions.promotion, "number_sessions": one_sessions.number_sessions, 'type_sessions': one_sessions.type_sessions, 'teacher': one_sessions.teacher}

  for one_planning in planning:
    remaining_session[one_planning.sessions.id]["number_sessions"] -= one_planning.number_sessions

  return render(request, 'management/edit-planning.html', {'week': week, 'year': year, 'remaining_session': remaining_session})

@login_required
def addPlanning(request, year_id, sessions_id):
  post_url = reverse('management:add-planning', args=(year_id, sessions_id))
  back_url = reverse('management:edit-planning', args=(year_id,))

  if request.method == 'POST':
    form = AddPlanning(request.POST, year_id=year_id)
    if form.is_valid():
      remaining_session = Sessions.objects.get(pk=sessions_id).number_sessions

      for one_planning in Planning.objects.filter(sessions=sessions_id):
        remaining_session -= one_planning.number_sessions

      if (form.cleaned_data['number_sessions'] > remaining_session):
        return render(request, 'management/add-form.html', {'form': form, 'error': 'Vous ne pouvez pas affecter plus de ' + str(remaining_session) + ' séances', 'post_url': post_url, "back_url": back_url})
      
      sessions = Sessions.objects.get(pk=sessions_id)
      Planning(sessions=sessions, week=form.cleaned_data['week'], number_sessions=form.cleaned_data['number_sessions']).save()
      return HttpResponseRedirect(reverse('management:edit-planning', args=(year_id,)))
  else:
    form = AddPlanning(year_id=year_id)
    return render(request, 'management/add-form.html', {'form': form, 'post_url': post_url, "back_url": back_url})

  #return HttpResponse("ok")
