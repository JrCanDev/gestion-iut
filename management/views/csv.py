import csv

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from management.forms import UploadFileForm
from management.models import Week, Teacher, Promotion, Planning


@login_required
@user_passes_test(lambda u: u.is_superuser)
def exporting_csv(request):
    """
    year = Year.objects.all()
    subject = Subject.objects.all()
    sessions = Sessions.objects.all()
    planning = Planning.objects.all()

    wb = openpyxl.Workbook()
    wb.create_sheet("Year").title = "Year"
    wb.create_sheet("Semester").title = "Semester"
    wb.create_sheet("Subject").title = "Subject"
    wb.create_sheet("Sessions").title = "Sessions"
    wb.create_sheet("Planning").title = "Planning"

    sheet = wb["Year"]
    row_year = ["name_year", "name_semester"]

    for i in range(0, len(row_year)):
        sheet.cell(row=(i + 1), column=1).value = row_year[i]

    for i in range(0, len(year)):
        sheet.cell(row=1, column=(i + 2)).value = year[i].name_year

        semester = ""
        for one_semester in year[i].semester_set.all():
            semester += (("," if len(semester) else "") + str(one_semester.name_semester))

        sheet.cell(row=2, column=(i + 2)).value = str(semester)

    sheet = wb["Subject"]
    row_subject = ["name_subject", "description", "number_cm_sessions", "number_td_sessions", "number_tp_sessions",
                   "promotion", "semester"]

    for i in range(0, len(row_subject)):
        sheet.cell(row=(i + 1), column=1).value = row_subject[i]

    for i in range(0, len(subject)):
        sheet.cell(row=1, column=(i + 2)).value = subject[i].name_subject
        sheet.cell(row=2, column=(i + 2)).value = subject[i].description
        sheet.cell(row=3, column=(i + 2)).value = subject[i].number_cm_sessions
        sheet.cell(row=4, column=(i + 2)).value = subject[i].number_td_sessions
        sheet.cell(row=5, column=(i + 2)).value = subject[i].number_tp_sessions
        sheet.cell(row=6, column=(i + 2)).value = subject[i].promotion.name_promotion
        sheet.cell(row=7, column=(i + 2)).value = subject[i].semester.name_semester

    sheet = wb["Sessions"]
    row_sessions = ["type_sessions", "teacher", "number_hours", "promotion", "td", "tp", "subject"]

    for i in range(0, len(row_sessions)):
        sheet.cell(row=(i + 1), column=1).value = row_sessions[i]

    for i in range(0, len(sessions)):
        sheet.cell(row=1, column=(i + 2)).value = sessions[i].type_sessions
        sheet.cell(row=2, column=(i + 2)).value = sessions[i].teacher.last_name
        sheet.cell(row=3, column=(i + 2)).value = sessions[i].number_hours
        sheet.cell(row=4, column=(i + 2)).value = sessions[i].promotion.name_promotion
        sheet.cell(row=5, column=(i + 2)).value = sessions[i].td.name_td if sessions[i].td else None

        tp = ""
        for one_tp in sessions[i].tp.all():
            tp += (("," if len(tp) else "") + one_tp.name_tp)

        sheet.cell(row=6, column=(i + 2)).value = str(tp)
        sheet.cell(row=7, column=(i + 2)).value = sessions[i].subject.name_subject

    sheet = wb["Planning"]
    row_planning = ["sessions", "number_hours", "week"]

    for i in range(0, len(row_planning)):
        sheet.cell(row=(i + 1), column=1).value = row_planning[i]

    for i in range(0, len(planning)):
        sheet.cell(row=1, column=(i + 2)).value = planning[i].sessions.id
        sheet.cell(row=2, column=(i + 2)).value = planning[i].number_hours
        sheet.cell(row=3, column=(i + 2)).value = planning[i].week.name_week

    wb.save("test.xlsx")

    row_subject = [["name_subject", "description", "number_cm_sessions", "number_td_sessions", "number_tp_sessions",
                    "promotion", "semester"]]

    for one_subject in subject:
        row_subject.append([one_subject.name_subject, one_subject.description, one_subject.number_cm_sessions,
                            one_subject.number_td_sessions, one_subject.number_tp_sessions, one_subject.promotion,
                            one_subject.semester])

    print(row_subject)

    with open('test.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_subject)
    """

    row_csv = [["name_year", "name_semester", "name_week"]]

    for one_week in Week.objects.all():
        row_csv.append([one_week.semester.year.name_year, one_week.semester.name_semester, one_week.name_week])

    with open('weeks.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_csv)

    row_csv = [["last_name", "first_name", "status"]]

    for one_teacher in Teacher.objects.all():
        row_csv.append([one_teacher.last_name, one_teacher.first_name, one_teacher.status])

    with open('teacher.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_csv)

    row_csv = [["name_promotion", "year", "semester", "td", "tp"]]

    for one_promotion in Promotion.objects.all():
        for one_td in one_promotion.td_set.all():
            for one_tp in one_td.tp_set.all():
                row_csv.append(
                    [one_promotion.name_promotion, one_promotion.year.name_year, one_td.semester.name_semester,
                     one_td.name_td, one_tp.name_tp])

    with open('promotion.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_csv)

    row_csv = [
        ["name_promotion", "name_subject", "sessions_id", "type_sessions", "teacher", "number_hours", "td", "tp"]]

    for one_promotion in Promotion.objects.all():
        for one_subject in one_promotion.subject_set.all():
            for one_sessions in one_subject.sessions_set.all():
                if one_sessions.tp.all():
                    for one_tp in one_sessions.tp.all():
                        row_csv.append([one_promotion.name_promotion, one_subject.name_subject, one_sessions.id,
                                        one_sessions.type_sessions, one_sessions.teacher.last_name,
                                        one_sessions.number_hours, one_sessions.td, one_tp])
                else:
                    row_csv.append([one_promotion.name_promotion, one_subject.name_subject, one_sessions.type_sessions,
                                    one_sessions.teacher.last_name, one_sessions.number_hours, one_sessions.td, ""])

    with open('sessions.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_csv)

    row_csv = [["name_subject", "sessions_id", "number_hours", "name_week"]]

    for one_planning in Planning.objects.all():
        row_csv.append([one_planning.sessions.subject.name_subject, one_planning.sessions.id, one_planning.number_hours,
                        one_planning.week.name_week])

    with open('planning.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_csv)

    return HttpResponse("ok")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def import_csv(request):
    post_url = reverse('management:import-csv')
    back_url = reverse('management:index')

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            return HttpResponse("ok")
        else:
            return HttpResponse(str(form.errors))
    else:
        form = UploadFileForm()
        return render(request, 'management/add-form.html', {'form': form, 'post_url': post_url, "back_url": back_url})
