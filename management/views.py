from hashlib import new
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from management.forms import AddPromotion, AddTeacher, AddYear, AddTD, AddTP, AddSubject, AddCmSubject, AddTdSubject, AddTpSubject
from management.models import Promotion, Subject, Teacher, Year, Td, Tp, Sessions


def index(request):
  year = Year.objects.all()
  teacher = Teacher.objects.all()
  promotion = Promotion.objects.all()
  
  return render(request, 'management/index.html', {'year': year, 'teacher': teacher, 'promotion': promotion})

def addYear(request):
  if request.method == 'POST':
    form = AddYear(request.POST)
    if form.is_valid():
      if (len(Year.objects.filter(name_year=form.cleaned_data['name_year']).all())):
       return render(request, 'management/add-year.html', {'form': form, 'error': 'L\'année existe déjà' })
      
      Year(name_year = form.cleaned_data['name_year']).save()
      return HttpResponseRedirect('/')
  else:
    form = AddYear()
    return render(request, 'management/add-year.html', {'form': form})

def addTeacher(request):
  if request.method == 'POST':
    form = AddTeacher(request.POST)
    if form.is_valid():
      if (len(Teacher.objects.filter(lastname=form.cleaned_data['lastname'], firstname=form.cleaned_data['firstname']).all())):
        return render(request, 'management/add-teacher.html', {'form': form, 'error': 'Le professeur existe déjà' })
      
      StatusChoices = {
        "1": "professeur",
        "2": "vacataire"
      }

      Teacher(lastname=form.cleaned_data['lastname'], firstname=form.cleaned_data['firstname'], status = StatusChoices[form.cleaned_data['status']]).save()
      return HttpResponseRedirect('/')
  else:
    form = AddTeacher()
    return render(request, 'management/add-teacher.html', {'form': form})

def addPromotion(request):
  if request.method == 'POST':
    form = AddPromotion(request.POST)
    if form.is_valid():
      if (len(Promotion.objects.filter(name_promotion=form.cleaned_data['name_promotion']).all())):
        return render(request, 'management/add-promotion.html', {'form': form, 'error': 'La promotion existe déjà' })
      
      new_promotion = Promotion(name_promotion=form.cleaned_data['name_promotion'], year=form.cleaned_data['year'])
      new_promotion.save()
      return HttpResponseRedirect(reverse('management:edit-promotion', args=(new_promotion.id,)))
  else:
    form = AddPromotion()
    return render(request, 'management/add-promotion.html', {'form': form})

def editPromotion(request, promotion_id):
  promotion = Promotion.objects.get(pk=promotion_id)
  td = promotion.td_set.all()
  subject = promotion.subject_set.all()
  return render(request, 'management/edit-promotion.html', {'promotion': promotion, 'td': td, 'subject': subject})

def addTd(request, promotion_id):
  if request.method == 'POST':
    form = AddTD(request.POST)
    if form.is_valid():
      if (len(Td.objects.filter(name_td=form.cleaned_data['name_td'], promotion=promotion_id).all())):
        return render(request, 'management/add-td.html', {'promotion_id': promotion_id, 'form': form, 'error': 'Le TD existe déjà' })

      promotion = Promotion.objects.get(pk=promotion_id)
      new_td = Td(name_td=form.cleaned_data['name_td'], promotion=promotion)
      new_td.save()
    return HttpResponseRedirect(reverse('management:edit-promotion', args=(promotion_id,)))
  else:
    form = AddTD()
    return render(request, 'management/add-td.html', {'promotion_id': promotion_id, 'form': form})

def editTd(request, promotion_id, td_id):
  promotion = Promotion.objects.get(pk=promotion_id)
  td = Td.objects.get(pk=td_id)

  return render(request, 'management/edit-td.html', {'promotion': promotion, 'td': td})

def addTp(request, promotion_id, td_id):
  if request.method == 'POST':
    form = AddTP(request.POST)
    if form.is_valid():
      list_tp = []

      for one_td in Td.objects.filter(promotion=promotion_id).all():
        for one_tp in one_td.tp_set.all():
          list_tp.append(one_tp.name_tp)
      
      if form.cleaned_data['name_tp'] in list_tp:
        return render(request, 'management/add-tp.html', {'promotion_id': promotion_id, 'td_id': td_id, 'form': form, 'error': 'Le TP existe déjà' })

      td = Td.objects.get(pk=td_id)
      new_tp = Tp(name_tp=form.cleaned_data['name_tp'], td=td)
      new_tp.save()
    return HttpResponseRedirect(reverse('management:edit-td', args=(promotion_id, td_id)))
  else:
    form = AddTP()
    return render(request, 'management/add-tp.html', {'promotion_id': promotion_id, 'td_id': td_id, 'form': form})

def editYear(request, year_id):
  year = Year.objects.get(pk=year_id)

  return render(request, 'management/edit-year.html', {'year': year})

def addSubject(request, promotion_id):
  if request.method == 'POST':
    form = AddSubject(request.POST)
    if form.is_valid():
      if (len(Subject.objects.filter(name_subject=form.cleaned_data['name_subject'], promotion=promotion_id).all())):
        return render(request, 'management/add-subject.html', {'promotion_id': promotion_id, 'form': form, 'error': 'La matiere existe déjà' })

      promotion = Promotion.objects.get(pk=promotion_id)
      new_subject = Subject(name_subject=form.cleaned_data['name_subject'], number_cm_sessions=form.cleaned_data['number_cm_sessions'],  number_td_sessions=form.cleaned_data['number_td_sessions'],  number_tp_sessions=form.cleaned_data['number_tp_sessions'], promotion=promotion)
      new_subject.save()
      return HttpResponseRedirect(reverse('management:edit-promotion', args=(promotion_id,)))
  else:
    form = AddSubject()
    return render(request, 'management/add-subject.html', {'promotion_id': promotion_id, 'form': form})

def editSubject(request, promotion_id, subject_id):
  subject = Subject.objects.get(pk=subject_id)
  promotion = Promotion.objects.get(pk=promotion_id)

  nb_sessions = {}

  nb_sessions["cm"] = {"for_promotion": subject.number_cm_sessions, "remaining": subject.number_cm_sessions}
  nb_sessions["td"] = {"for_td": subject.number_td_sessions, "remaining": (subject.number_td_sessions * len(promotion.td_set.all()))}
  nb_sessions["tp"] = {"for_tp": subject.number_tp_sessions, "remaining": 0}

  for one_td in promotion.td_set.all():
    nb_sessions["tp"]["remaining"] += (subject.number_tp_sessions * len(one_td.tp_set.all()))

  for one_sessions in subject.sessions_set.all():
    if(one_sessions.type_sessions == "cm"):
      nb_sessions["cm"]["remaining"] -= one_sessions.number_sessions
    if(one_sessions.type_sessions == "td"):
      nb_sessions["td"]["remaining"] -= one_sessions.number_sessions
    if(one_sessions.type_sessions == "tp"):
      nb_sessions["tp"]["remaining"] -= one_sessions.number_sessions
  
  
  session_td = {}
  session_tp = {}

  for one_td in promotion.td_set.all():
    session_td[one_td] = (subject.sessions_set.filter(td=one_td).all())

    for one_tp in one_td.tp_set.all():
      session_tp[one_tp] = (subject.sessions_set.filter(tp=one_tp).all())

  return render(request, 'management/edit-subject.html', {'promotion': promotion, 'subject': subject, 'nb_sessions': nb_sessions, "session_td": session_td, "session_tp": session_tp})

def addCmSession(request, promotion_id, subject_id):
  if request.method == 'POST':
    form = AddCmSubject(request.POST)
    if form.is_valid():
      subject = Subject.objects.get(pk=subject_id)
      nb_sessions_remaining = subject.number_cm_sessions
      promotion = Promotion.objects.get(pk=promotion_id)

      for one_sessions in subject.sessions_set.all():
        if(one_sessions.type_sessions == "cm"):
          nb_sessions_remaining -= one_sessions.number_sessions
      
      if form.cleaned_data['number_sessions'] > nb_sessions_remaining:
        return render(request, 'management/add-cm-session.html', {'promotion_id': promotion_id, 'subject_id': subject_id, 'form': form, 'error': 'Vous ne pouvez pas affecter plus de ' + str(nb_sessions_remaining) + ' séances' })

      new_session = Sessions(subject=subject, type_sessions='cm', teacher=form.cleaned_data['teacher'], number_sessions=form.cleaned_data['number_sessions'], promotion=promotion)
      new_session.save()
      return HttpResponseRedirect(reverse('management:edit-subject', args=(promotion_id, subject_id)))
  else:
    form = AddCmSubject()
    return render(request, 'management/add-cm-session.html', {'promotion_id': promotion_id, 'subject_id': subject_id, 'form': form})

def addTdSession(request, promotion_id, subject_id):
  if request.method == 'POST':
    form = AddTdSubject(request.POST, promotion_id=promotion_id)
    if form.is_valid():
      subject = Subject.objects.get(pk=subject_id)
      promotion = Promotion.objects.get(pk=promotion_id)
      nb_sessions_remaining = subject.number_td_sessions

      for one_sessions in subject.sessions_set.filter(td=form.cleaned_data['td']).all():
        if(one_sessions.type_sessions == "td"):
          nb_sessions_remaining -= one_sessions.number_sessions
      
      if form.cleaned_data['number_sessions'] > nb_sessions_remaining:
        return render(request, 'management/add-td-session.html', {'promotion_id': promotion_id, 'subject_id': subject_id, 'form': form, 'error': 'Vous ne pouvez pas affecter plus de ' + str(nb_sessions_remaining) + ' séances' })

      new_session = Sessions(subject=subject, type_sessions='td', teacher=form.cleaned_data['teacher'], number_sessions=form.cleaned_data['number_sessions'], td=form.cleaned_data['td'])
      new_session.save()
      return HttpResponseRedirect(reverse('management:edit-subject', args=(promotion_id, subject_id)))
  else:
    form = AddTdSubject(promotion_id=promotion_id)
    return render(request, 'management/add-td-session.html', {'promotion_id': promotion_id, 'subject_id': subject_id, 'form': form})

def addTpSession(request, promotion_id, subject_id):
  if request.method == 'POST':
    form = AddTpSubject(request.POST, promotion_id=promotion_id)
    if form.is_valid():
      subject = Subject.objects.get(pk=subject_id)
      promotion = Promotion.objects.get(pk=promotion_id)
      nb_sessions_remaining = subject.number_tp_sessions

      for one_sessions in subject.sessions_set.filter(tp=form.cleaned_data['tp']).all():
        if(one_sessions.type_sessions == "tp"):
          nb_sessions_remaining -= one_sessions.number_sessions
        
      if form.cleaned_data['number_sessions'] > nb_sessions_remaining:
        return render(request, 'management/add-tp-session.html', {'promotion_id': promotion_id, 'subject_id': subject_id, 'form': form, 'error': 'Vous ne pouvez pas affecter plus de ' + str(nb_sessions_remaining) + ' séances' })

      new_session = Sessions(subject=subject, type_sessions='tp', teacher=form.cleaned_data['teacher'], number_sessions=form.cleaned_data['number_sessions'])
      tp = Tp.objects.get(pk=form.cleaned_data['tp'].id)
      new_session.save()
      new_session.tp.add(tp)
      new_session.save()
      return HttpResponseRedirect(reverse('management:edit-subject', args=(promotion_id, subject_id)))
  else:
    form = AddTpSubject(promotion_id=promotion_id)
    return render(request, 'management/add-tp-session.html', {'promotion_id': promotion_id, 'subject_id': subject_id, 'form': form})

  #return HttpResponse("Hello, world. You're at the polls index.")
  