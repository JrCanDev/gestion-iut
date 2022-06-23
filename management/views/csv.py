import csv
import shutil

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from management.forms import UploadFileForm
from management.models import Week, Teacher, Promotion, Year, Semester, Td, Tp, Subject, Sessions, Planning


@login_required
@user_passes_test(lambda u: u.is_superuser)
def exporting_csv(request):
    row_csv = [["name_year", "name_semester", "name_week"]]

    for one_week in Week.objects.all():
        row_csv.append([one_week.semester.year.name_year, one_week.semester.name_semester, one_week.name_week])

    with open('tmp/csv/weeks.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_csv)

    row_csv = [["last_name", "first_name", "status"]]

    for one_teacher in Teacher.objects.all():
        row_csv.append([one_teacher.last_name, one_teacher.first_name, one_teacher.status])

    with open('tmp/csv/teacher.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_csv)

    row_csv = [["name_promotion", "year", "semester", "td", "tp"]]

    for one_promotion in Promotion.objects.all():
        for one_td in one_promotion.td_set.all():
            for one_tp in one_td.tp_set.all():
                row_csv.append(
                    [one_promotion.name_promotion, one_promotion.year.name_year, one_td.semester.name_semester,
                     one_td.name_td, one_tp.name_tp])

    with open('tmp/csv/promotion.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_csv)

    row_csv = [
        ["name_subject", "description", "number_cm_sessions", "number_td_sessions", "number_tp_sessions",
         "name_promotion", "name_semester", "name_year"]]

    for one_subject in Subject.objects.all():
        row_csv.append([one_subject.name_subject, one_subject.description, one_subject.number_cm_sessions,
                        one_subject.number_td_sessions, one_subject.number_tp_sessions,
                        one_subject.promotion.name_promotion, one_subject.semester.name_semester,
                        one_subject.semester.year.name_year])

    with open('tmp/csv/subject.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_csv)

    row_csv = [
        ["name_subject", "name_promotion", "name_teacher", "name_semester", "name_year", "type_sessions",
         "number_hours", "name_td", "name_tp"]]

    for one_sessions in Sessions.objects.all():
        print(one_sessions.tp)
        if one_sessions.tp:
            row_csv.append([one_sessions.subject.name_subject, one_sessions.promotion.name_promotion,
                            one_sessions.teacher.last_name, one_sessions.subject.semester.name_semester,
                            one_sessions.subject.semester.year.name_year, one_sessions.type_sessions,
                            one_sessions.number_hours, "", one_sessions.tp.name_tp])
        elif one_sessions.td:
            row_csv.append([one_sessions.subject.name_subject, one_sessions.promotion.name_promotion,
                            one_sessions.teacher.last_name, one_sessions.subject.semester.name_semester,
                            one_sessions.subject.semester.year.name_year, one_sessions.type_sessions,
                            one_sessions.number_hours, one_sessions.td.name_td, ""])
        else:
            row_csv.append([one_sessions.subject.name_subject, one_sessions.promotion.name_promotion,
                            one_sessions.teacher.last_name, one_sessions.subject.semester.name_semester,
                            one_sessions.subject.semester.year.name_year, one_sessions.type_sessions,
                            one_sessions.number_hours, "", ""])

    with open('tmp/csv/sessions.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_csv)

    row_csv = [["number_hours_planning", "name_week", "name_semester", "name_year", "type_sessions", "name_teacher",
                "number_hours_sessions", "name_promotion", "name_subject", "name_td", "name_tp"]]

    for one_planning in Planning.objects.all():
        if one_planning.sessions.td:
            row_csv.append([one_planning.number_hours, one_planning.week.name_week,
                            one_planning.week.semester.name_semester, one_planning.week.semester.year.name_year,
                            one_planning.sessions.type_sessions, one_planning.sessions.teacher.last_name,
                            one_planning.sessions.number_hours, one_planning.sessions.promotion.name_promotion,
                            one_planning.sessions.subject.name_subject, one_planning.sessions.td.name_td, ""])
        elif one_planning.sessions.tp:
            row_csv.append([one_planning.number_hours, one_planning.week.name_week,
                            one_planning.week.semester.name_semester, one_planning.week.semester.year.name_year,
                            one_planning.sessions.type_sessions, one_planning.sessions.teacher.last_name,
                            one_planning.sessions.number_hours, one_planning.sessions.promotion.name_promotion,
                            one_planning.sessions.subject.name_subject, "", one_planning.sessions.tp.name_tp])
        else:
            row_csv.append([one_planning.number_hours, one_planning.week.name_week,
                            one_planning.week.semester.name_semester, one_planning.week.semester.year.name_year,
                            one_planning.sessions.type_sessions, one_planning.sessions.teacher.last_name,
                            one_planning.sessions.number_hours, one_planning.sessions.promotion.name_promotion,
                            one_planning.sessions.subject.name_subject, "", ""])

    with open('tmp/csv/planning.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_csv)

    shutil.make_archive('tmp/export', 'zip', 'tmp/csv')

    filepath = 'tmp/export.zip'
    file = open(filepath, 'rb')
    response = HttpResponse(file, content_type="application/zip")
    response['Content-Disposition'] = "attachment; filename=export.zip"
    return response


@login_required
@user_passes_test(lambda u: u.is_superuser)
def import_csv(request):
    post_url = reverse('management:import-csv')
    back_url = reverse('management:managed-settings')

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['weeks'], "weeks.csv")
            handle_uploaded_file(request.FILES['teacher'], "teacher.csv")
            handle_uploaded_file(request.FILES['promotion'], "promotion.csv")
            handle_uploaded_file(request.FILES['subject'], "subject.csv")
            handle_uploaded_file(request.FILES['sessions'], "sessions.csv")
            handle_uploaded_file(request.FILES['planning'], "planning.csv")

            with open('tmp/csv/weeks.csv', mode='r') as file:
                csv_file = csv.reader(file)
                next(csv_file)

                for one_lines in csv_file:
                    if not Year.objects.filter(name_year=one_lines[0]).first():
                        Year(name_year=one_lines[0]).save()

                    if not Semester.objects.filter(name_semester=one_lines[1], year__name_year=one_lines[0]).first():
                        Semester(name_semester=one_lines[1], year=Year.objects.get(name_year=one_lines[0])).save()

                    if not Week.objects.filter(name_week=one_lines[2], semester__name_semester=one_lines[1]).first():
                        Week(name_week=one_lines[2],
                             semester=Semester.objects.get(name_semester=one_lines[1],
                                                           year=Year.objects.get(name_year=one_lines[0]))).save()

            with open('tmp/csv/teacher.csv', mode='r') as file:
                csv_file = csv.reader(file)
                next(csv_file)

                for one_lines in csv_file:
                    if not Teacher.objects.filter(last_name=one_lines[0]).first():
                        user = Teacher.objects.create_user(one_lines[0], '', '')
                        user.last_name = one_lines[0]
                        user.first_name = one_lines[1]
                        user.status = one_lines[2]
                        user.save()

            with open('tmp/csv/promotion.csv', mode='r') as file:
                csv_file = csv.reader(file)
                next(csv_file)

                for one_lines in csv_file:
                    if not Year.objects.filter(name_year=one_lines[1]).first():
                        return render(request, 'management/add-form.html',
                                      {'form': form, 'post_url': post_url, "back_url": back_url,
                                       "error": "l'année " + one_lines[1] + " n'existe pas"})

                    if not Semester.objects.filter(name_semester=one_lines[2], year__name_year=one_lines[1]).first():
                        year = Year.objects.filter(name_year=one_lines[1]).first()
                        Semester(year=year, name_semester=one_lines[2]).save()

                    if not Promotion.objects.filter(name_promotion=one_lines[0]).first():
                        year = Year.objects.filter(name_year=one_lines[1]).first()
                        Promotion(name_promotion=one_lines[0], year=year).save()

                    if not Td.objects.filter(name_td=one_lines[3], promotion__name_promotion=one_lines[0],
                                             semester__name_semester=one_lines[2]).first():
                        promotion = Promotion.objects.filter(name_promotion=one_lines[0],
                                                             year__name_year=one_lines[1]).first()
                        semester = Semester.objects.filter(name_semester=one_lines[2],
                                                           year__name_year=one_lines[1]).first()

                        Td(name_td=one_lines[3], semester=semester, promotion=promotion).save()

                    td = Td.objects.filter(name_td=one_lines[3], promotion__name_promotion=one_lines[0],
                                           semester__name_semester=one_lines[2]).first()

                    if not Tp.objects.filter(name_tp=one_lines[4], td=td).first():
                        Tp(name_tp=one_lines[4], td=td).save()

            with open('tmp/csv/subject.csv', mode='r') as file:
                csv_file = csv.reader(file)
                next(csv_file)

                for one_lines in csv_file:
                    if not Promotion.objects.filter(name_promotion=one_lines[5], year__name_year=one_lines[7]).first():
                        return render(request, 'management/add-form.html',
                                      {'form': form, 'post_url': post_url, "back_url": back_url,
                                       "error": "la promotion " + one_lines[5] + " n'existe pas"})

                    if not Semester.objects.filter(name_semester=one_lines[6], year__name_year=one_lines[7]).first():
                        return render(request, 'management/add-form.html',
                                      {'form': form, 'post_url': post_url, "back_url": back_url,
                                       "error": "le semestre " + one_lines[6] + " n'existe pas"})

                    if not Subject.objects.filter(name_subject=one_lines[0], promotion__name_promotion=one_lines[5],
                                                  semester__name_semester=one_lines[6],
                                                  semester__year__name_year=one_lines[7]).first():
                        promotion = Promotion.objects.filter(name_promotion=one_lines[5],
                                                             year__name_year=one_lines[7]).first()
                        semester = Semester.objects.filter(name_semester=one_lines[6],
                                                           year__name_year=one_lines[7]).first()

                        Subject(name_subject=one_lines[0], description=one_lines[1], number_cm_sessions=one_lines[2],
                                number_td_sessions=one_lines[3], number_tp_sessions=one_lines[4], promotion=promotion,
                                semester=semester).save()

            with open('tmp/csv/sessions.csv', mode='r') as file:
                csv_file = csv.reader(file)
                next(csv_file)

                for one_lines in csv_file:
                    promotion = Promotion.objects.filter(name_promotion=one_lines[1],
                                                         year__name_year=one_lines[4]).first()

                    if not promotion:
                        return render(request, 'management/add-form.html',
                                      {'form': form, 'post_url': post_url, "back_url": back_url,
                                       "error": "la promotion " + one_lines[1] + " n'existe pas"})

                    semester = Semester.objects.filter(name_semester=one_lines[3], year__name_year=one_lines[4]).first()
                    if not promotion:
                        return render(request, 'management/add-form.html',
                                      {'form': form, 'post_url': post_url, "back_url": back_url,
                                       "error": "le semestre " + one_lines[3] + " n'existe pas"})

                    subject = Subject.objects.filter(name_subject=one_lines[0], semester=semester,
                                                     promotion=promotion).first()

                    if not subject:
                        return render(request, 'management/add-form.html',
                                      {'form': form, 'post_url': post_url, "back_url": back_url,
                                       "error": "la ressource " + one_lines[0] + " n'existe pas"})

                    teacher = Teacher.objects.filter(last_name=one_lines[2]).first()

                    if not teacher:
                        return render(request, 'management/add-form.html',
                                      {'form': form, 'post_url': post_url, "back_url": back_url,
                                       "error": "le professeur " + one_lines[2] + " n'existe pas"})

                    if one_lines[5] == "cm":
                        if not Sessions.objects.filter(type_sessions="cm", teacher=teacher, number_hours=one_lines[6],
                                                       promotion=promotion, subject=subject).first():
                            Sessions(type_sessions="cm", teacher=teacher, number_hours=one_lines[6],
                                     promotion=promotion, subject=subject).save()
                    elif one_lines[5] == "td":
                        td = Td.objects.filter(name_td=one_lines[7], promotion=promotion, semester=semester).first()

                        if not td:
                            return render(request, 'management/add-form.html',
                                          {'form': form, 'post_url': post_url, "back_url": back_url,
                                           "error": "le td " + one_lines[7] + " n'existe pas"})

                        if not Sessions.objects.filter(type_sessions="td", teacher=teacher, number_hours=one_lines[6],
                                                       promotion=promotion, subject=subject, td=td).first():
                            Sessions(type_sessions="td", teacher=teacher, number_hours=one_lines[6],
                                     promotion=promotion, subject=subject, td=td).save()
                    elif one_lines[5] == "tp":
                        tp = Tp.objects.filter(name_tp=one_lines[8], td__semester__name_semester=one_lines[3],
                                               td__promotion__name_promotion=one_lines[1]).first()

                        if not tp:
                            return render(request, 'management/add-form.html',
                                          {'form': form, 'post_url': post_url, "back_url": back_url,
                                           "error": "le tp " + one_lines[8] + " n'existe pas"})

                        if not Sessions.objects.filter(type_sessions="tp", teacher=teacher, number_hours=one_lines[6],
                                                       promotion=promotion, subject=subject,
                                                       tp=tp).first():
                            Sessions(type_sessions="tp", teacher=teacher, number_hours=one_lines[6],
                                     promotion=promotion, subject=subject, tp=tp).save()

            with open('tmp/csv/planning.csv', mode='r') as file:
                csv_file = csv.reader(file)
                next(csv_file)

                for one_lines in csv_file:
                    year = Year.objects.filter(name_year=one_lines[3]).first()

                    if not year:
                        return render(request, 'management/add-form.html',
                                      {'form': form, 'post_url': post_url, "back_url": back_url,
                                       "error": "l'année " + one_lines[3] + " n'existe pas"})

                    semester = Semester.objects.filter(name_semester=one_lines[2], year=year).first()

                    if not semester:
                        return render(request, 'management/add-form.html',
                                      {'form': form, 'post_url': post_url, "back_url": back_url,
                                       "error": "le semestre " + one_lines[2] + " n'existe pas"})

                    week = Week.objects.filter(name_week=one_lines[1], semester=semester).first()

                    if not week:
                        return render(request, 'management/add-form.html',
                                      {'form': form, 'post_url': post_url, "back_url": back_url,
                                       "error": "le semaine " + one_lines[1] + " n'existe pas"})

                    promotion = Promotion.objects.filter(name_promotion=one_lines[7], year=year).first()

                    if not promotion:
                        return render(request, 'management/add-form.html',
                                      {'form': form, 'post_url': post_url, "back_url": back_url,
                                       "error": "la promotion " + one_lines[7] + " n'existe pas"})

                    print(one_lines[8], promotion, semester)
                    subject = Subject.objects.filter(name_subject=one_lines[8], promotion=promotion,
                                                     semester=semester).first()

                    if not subject:
                        return render(request, 'management/add-form.html',
                                      {'form': form, 'post_url': post_url, "back_url": back_url,
                                       "error": "la ressource " + one_lines[8] + " n'existe pas"})

                    teacher = Teacher.objects.filter(last_name=one_lines[5]).first()

                    if not subject:
                        return render(request, 'management/add-form.html',
                                      {'form': form, 'post_url': post_url, "back_url": back_url,
                                       "error": "le professeur " + one_lines[5] + " n'existe pas"})

                    if one_lines[4] == "cm":
                        sessions = Sessions.objects.filter(type_sessions=one_lines[4], teacher=teacher,
                                                           number_hours=one_lines[6], promotion=promotion,
                                                           subject=subject).first()

                        if not Sessions:
                            return render(request, 'management/add-form.html',
                                          {'form': form, 'post_url': post_url, "back_url": back_url,
                                           "error": "la sessions n'existe pas"})

                        if not Planning.objects.filter(sessions=sessions, number_hours=one_lines[0],
                                                       week=week).filter():
                            Planning(sessions=sessions, number_hours=one_lines[0], week=week).save()
                    elif one_lines[4] == "td":
                        td = Td.objects.filter(name_td=one_lines[9], promotion=promotion, semester=semester).first()

                        if not td:
                            return render(request, 'management/add-form.html',
                                          {'form': form, 'post_url': post_url, "back_url": back_url,
                                           "error": "le td " + one_lines[9] + " n'existe pas"})

                        sessions = Sessions.objects.filter(type_sessions=one_lines[4], teacher=teacher,
                                                           number_hours=one_lines[6], promotion=promotion,
                                                           subject=subject, td=td).first()

                        if not Sessions:
                            return render(request, 'management/add-form.html',
                                          {'form': form, 'post_url': post_url, "back_url": back_url,
                                           "error": "la sessions n'existe pas"})

                        if not Planning.objects.filter(sessions=sessions, number_hours=one_lines[0],
                                                       week=week).filter():
                            Planning(sessions=sessions, number_hours=one_lines[0], week=week).save()
                    elif one_lines[4] == "tp":
                        tp = Tp.objects.filter(name_tp=one_lines[10], tp__promotion__name_promotion=promotion,
                                               td__semester__name_semester=semester).first()

                        if not tp:
                            return render(request, 'management/add-form.html',
                                          {'form': form, 'post_url': post_url, "back_url": back_url,
                                           "error": "le td " + one_lines[10] + " n'existe pas"})

                        sessions = Sessions.objects.filter(type_sessions=one_lines[4], teacher=teacher,
                                                           number_hours=one_lines[6], promotion=promotion,
                                                           subject=subject, tp=tp).first()

                        if not Sessions:
                            return render(request, 'management/add-form.html',
                                          {'form': form, 'post_url': post_url, "back_url": back_url,
                                           "error": "la sessions n'existe pas"})

                        if not Planning.objects.filter(sessions=sessions, number_hours=one_lines[0],
                                                       week=week).filter():
                            Planning(sessions=sessions, number_hours=one_lines[0], week=week).save()

            return HttpResponseRedirect(reverse('management:managed-settings', args=()))
        else:
            return HttpResponse(str(form.errors))
    else:
        form = UploadFileForm()
        return render(request, 'management/add-form.html', {'form': form, 'post_url': post_url, "back_url": back_url})


def handle_uploaded_file(f, name):
    with open('tmp/csv/' + name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
