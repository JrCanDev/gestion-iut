from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from management.forms import AddTeacher, DeleteForm
from management.models import Teacher, Year


@login_required
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
            user.save()
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
    year = Year.objects.all()

    return render(request, 'management/managed-teacher.html', {'teacher': teacher, 'year': year})


@login_required
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
