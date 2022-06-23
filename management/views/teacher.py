import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from management.forms import AddTeacher, DeleteForm, EditTeacher
from management.models import Teacher, Year


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_teacher(request):
    """
    Affiche la vue responsable de l'ajout d'un professeur et gère le retour de celle-ci.
    """
    post_url = reverse('management:add-teacher', args=())
    back_url = reverse('management:index', args=())

    if request.method == 'POST':
        form = AddTeacher(request.POST)
        if form.is_valid():
            '''
            Si le formulaire a été soumi, on vérifie que les champs ont été correctement remplis.
            '''

            if (len(Teacher.objects.filter(last_name=form.cleaned_data['last_name'],
                                           first_name=form.cleaned_data['first_name']).all())):
                '''
                Si le professeur existe déjà on revoie le formulaire avec une erreur.
                '''

                return render(request, 'management/add-form.html',
                              {'form': form, 'error': 'Le professeur existe déjà', 'post_url': post_url,
                               "back_url": back_url})

            status_choices = {
                "1": "professeur",
                "2": "vacataire"
            }

            '''
            Ajoute les données à la BDD et redirige le client.
            '''
            user = Teacher.objects.create_user(form.cleaned_data['last_name'], '', form.cleaned_data['password'])
            user.last_name = form.cleaned_data['last_name']
            user.first_name = form.cleaned_data['first_name']
            user.status = status_choices[form.cleaned_data['status']]
            user.is_superuser = form.cleaned_data['admin']
            user.save()
            print(user.is_superuser)
            return HttpResponseRedirect('/')
    else:
        '''
        Sinon on affiche le formulaire vide.
        '''

        form = AddTeacher()
        return render(request, 'management/add-form.html', {'form': form, 'post_url': post_url, "back_url": back_url})


@login_required
def managed_teacher(request, teacher_id):
    teacher = Teacher.objects.get(pk=teacher_id)
    year = Year.objects.all().order_by("-name_year")

    file = open('settings.json')
    settings = json.load(file)

    services = {}

    for one_year in year:
        services[one_year.name_year] = {"total": {"cm": 0.0, "td": 0.0, "tp": 0.0}, "sessions": {}, "cost": 0.0}

    for one_session in teacher.sessions_set.all():
        sessions_year = one_session.promotion.year.name_year
        name_subject = one_session.subject.name_subject

        if name_subject not in services[sessions_year]["sessions"]:
            services[sessions_year]["sessions"][name_subject] = {"cm": 0.0, "td": 0.0, "tp": 0.0}

        if one_session.type_sessions == "cm":
            services[sessions_year]["total"]["cm"] += one_session.number_hours
            services[sessions_year]["sessions"][name_subject]["cm"] += one_session.number_hours
            services[sessions_year]["cost"] += ((settings[one_session.teacher.status]["hour_price"] *
                                                 settings[one_session.teacher.status]["eq_td"]["cm"]) *
                                                one_session.number_hours)

        elif one_session.type_sessions == "td":
            services[sessions_year]["total"]["td"] += one_session.number_hours
            services[sessions_year]["sessions"][name_subject]["td"] += one_session.number_hours
            services[sessions_year]["cost"] += ((settings[one_session.teacher.status]["hour_price"] *
                                                 settings[one_session.teacher.status]["eq_td"]["td"]) *
                                                one_session.number_hours)

        elif one_session.type_sessions == "tp":
            services[sessions_year]["total"]["tp"] += one_session.number_hours
            services[sessions_year]["sessions"][name_subject]["td"] += one_session.number_hours
            services[sessions_year]["cost"] += ((settings[one_session.teacher.status]["hour_price"] *
                                                 settings[one_session.teacher.status]["eq_td"]["tp"]) *
                                                one_session.number_hours)

    return render(request, 'management/managed-teacher.html', {'teacher': teacher, 'services': services})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_teacher(request, teacher_id):
    post_url = reverse('management:edit-teacher', args=(teacher_id,))
    back_url = reverse('management:index')

    teacher = Teacher.objects.get(pk=teacher_id)

    if request.method == 'POST':
        form = EditTeacher(request.POST, teacher=teacher)
        if form.is_valid():
            '''
            Si le formulaire a été soumi, on vérifie que les champs ont été correctement remplis.
            '''

            status_choices = {
                "1": "professeur",
                "2": "vacataire"
            }

            '''
            Ajoute les données à la BDD et redirige le client.
            '''
            teacher.last_name = form.cleaned_data['last_name']
            teacher.first_name = form.cleaned_data['first_name']
            teacher.status = status_choices[form.cleaned_data['status']]
            teacher.is_superuser = form.cleaned_data['admin']
            teacher.save()
            return HttpResponseRedirect('/')
    else:
        '''
        Sinon on affiche le formulaire vide.
        '''

        form = EditTeacher(teacher=teacher)
        return render(request, 'management/edit-form.html', {'form': form, 'post_url': post_url, "back_url": back_url})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_teacher(request, teacher_id):
    post_url = reverse('management:delete-teacher', args=(teacher_id,))
    back_url = reverse('management:index', args=())

    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data['confirm']:
                return render(request, 'management/delete-form.html',
                              {'form': form, 'error': 'Vous devez confirmer la suppression', 'post_url': post_url,
                               "back_url": back_url})

            teacher = Teacher.objects.get(pk=teacher_id)
            teacher.delete()
            return HttpResponseRedirect(reverse('management:index', args=()))
    else:
        form = DeleteForm()
        return render(request, 'management/delete-form.html',
                      {'form': form, 'post_url': post_url, "back_url": back_url,
                       "info": "Tous les éléments liés à ce professeur seront aussi supprimés !"})
