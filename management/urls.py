from django.urls import path
from management.views import home, planning, promotion, semester, session, subject, td, teacher, tp, week, year

app_name = 'management'
urlpatterns = [
  path('', home.index, name='index'),
  path('accounts/login/', home.userLogin, name='login'),  

  path('add/year', year.addYear, name="add-year"),
  path('add/teacher', teacher.addTeacher, name="add-teacher"),
  path('add/promotion', promotion.addPromotion, name="add-promotion"),

  path('managed/promotion/<int:promotion_id>', promotion.managedPromotion, name="managed-promotion"),
  path('managed/promotion/<int:promotion_id>/add/td', td.addTd, name="add-td"),
  path('managed/promotion/<int:promotion_id>/managed/td/<int:td_id>', td.managedTd, name="managed-td"),
  path('managed/promotion/<int:promotion_id>/managed/td/<int:td_id>/add/tp', tp.addTp, name="add-tp"),
  path('managed/promotion/<int:promotion_id>/add/subject', subject.addSubject, name="add-subject"),
  path('managed/promotion/<int:promotion_id>/managed/subject/<int:subject_id>', subject.managedSubject, name="managed-subject"),
  path('managed/promotion/<int:promotion_id>/managed/subject/<int:subject_id>/add/session/cm', session.addCmSession, name="add-cm-session"),
  path('managed/promotion/<int:promotion_id>/managed/subject/<int:subject_id>/add/session/td', session.addTdSession, name="add-td-session"),
  path('managed/promotion/<int:promotion_id>/managed/subject/<int:subject_id>/add/session/tp', session.addTpSession, name="add-tp-session"),

  path('managed/year/<int:year_id>', year.managedYear, name="managed-year"),
  path('managed/year/<int:year_id>/add/semester', semester.addSemester, name="add-semester"),
  path('managed/year/<int:year_id>/managed/semester/<int:semester_id>', semester.managedSemester, name="managed-semester"),
  path('managed/year/<int:year_id>/managed/semester/<int:semester_id>/add/week', week.addWeek, name="add-week"),
  path('managed/year/<int:year_id>/managed/planning', planning.managedPlanning, name='managed-planning'),
  path('managed/year/<int:year_id>/add/planning/<int:sessions_id>', planning.addPlanning, name='add-planning'),

  path('managed/teacher/<int:teacher_id>', teacher.managedTeacher, name='managed-teacher'),

  path('delete/year/<int:year_id>', year.deleteYear, name='delete-year'),
  path('managed/year/<int:year_id>/delete/semester/<int:semester_id>', semester.deleteSemester, name='delete-semester'),
  path('managed/year/<int:year_id>/managed/semester/<int:semester_id>/delete/week<int:week_id>', week.deleteWeek, name="delete-week"),

  path('delete/teacher/<int:teacher_id>', teacher.deleteTeacher, name='delete-teacher'),

  path('delete/promotion/<int:promotion_id>', promotion.deletePromotion, name="delete-promotion"),
  path('managed/promotion/<int:promotion_id>/delete/td/<int:td_id>', td.deleteTd, name="delete-td"),
  path('managed/promotion/<int:promotion_id>/managed/td/<int:td_id>/delete/tp/<int:tp_id>', tp.deleteTp, name="delete-tp"),
  path('managed/promotion/<int:promotion_id>/delete/subject/<int:subject_id>', subject.deleteSubject, name="delete-subject"),
  path('managed/promotion/<int:promotion_id>/managed/subject/<int:subject_id>/delete/session/<int:session_id>', session.deleteSession, name="delete-session"),

  path('managed/year/<int:year_id>/delete/planning/<int:planning_id>', planning.deletePlanning, name='delete-planning'),
]
