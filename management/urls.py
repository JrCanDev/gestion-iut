from django.urls import path

from management.views import home, planning, promotion, semester, session, subject, td, teacher, tp, week, year

app_name = 'management'
urlpatterns = [
    path('', home.index, name='index'),
    path('accounts/login/', home.user_login, name='login'),
    path('accounts/logout/', home.user_logout, name='logout'),
    path('accounts/change/password/<int:teacher_id>', home.user_change_password, name='change-password'),

    path('add/year', year.add_year, name="add-year"),
    path('add/teacher', teacher.add_teacher, name="add-teacher"),
    path('add/promotion', promotion.add_promotion, name="add-promotion"),

    path('managed/promotion/<int:promotion_id>', promotion.managed_promotion, name="managed-promotion"),
    path('managed/promotion/<int:promotion_id>/add/td', td.add_td, name="add-td"),
    path('managed/promotion/<int:promotion_id>/managed/td/<int:td_id>', td.managed_td, name="managed-td"),
    path('managed/promotion/<int:promotion_id>/managed/td/<int:td_id>/add/tp', tp.add_tp, name="add-tp"),
    path('managed/promotion/<int:promotion_id>/add/subject', subject.add_subject, name="add-subject"),
    path('managed/promotion/<int:promotion_id>/edit/subject/<int:subject_id>', subject.edit_subject,
         name="edit-subject"),
    path('managed/promotion/<int:promotion_id>/managed/subject/<int:subject_id>', subject.managed_subject,
         name="managed-subject"),
    path('managed/promotion/<int:promotion_id>/managed/subject/<int:subject_id>/add/session/cm', session.add_cm_session,
         name="add-cm-session"),
    path('managed/promotion/<int:promotion_id>/managed/subject/<int:subject_id>/add/session/td', session.add_td_session,
         name="add-td-session"),
    path('managed/promotion/<int:promotion_id>/managed/subject/<int:subject_id>/add/session/tp', session.add_tp_session,
         name="add-tp-session"),

    path('managed/year/<int:year_id>', year.managed_year, name="managed-year"),
    path('managed/year/<int:year_id>/add/semester', semester.add_semester, name="add-semester"),
    path('managed/year/<int:year_id>/managed/semester/<int:semester_id>', semester.managed_semester,
         name="managed-semester"),
    path('managed/year/<int:year_id>/managed/semester/<int:semester_id>/add/week', week.add_week, name="add-week"),
    path('managed/year/<int:year_id>/managed/planning', planning.managed_planning, name='managed-planning'),
    path('managed/year/<int:year_id>/add/planning/<int:sessions_id>', planning.add_planning, name='add-planning'),

    path('managed/teacher/<int:teacher_id>', teacher.managed_teacher, name='managed-teacher'),
    path('edit/teacher/<int:teacher_id>', teacher.edit_teacher, name='edit-teacher'),

    path('delete/year/<int:year_id>', year.delete_year, name='delete-year'),
    path('managed/year/<int:year_id>/delete/semester/<int:semester_id>', semester.delete_semester,
         name='delete-semester'),
    path('managed/year/<int:year_id>/managed/semester/<int:semester_id>/delete/week<int:week_id>', week.delete_week,
         name="delete-week"),

    path('delete/teacher/<int:teacher_id>', teacher.delete_teacher, name='delete-teacher'),

    path('delete/promotion/<int:promotion_id>', promotion.delete_promotion, name="delete-promotion"),
    path('managed/promotion/<int:promotion_id>/delete/td/<int:td_id>', td.delete_td, name="delete-td"),
    path('managed/promotion/<int:promotion_id>/managed/td/<int:td_id>/delete/tp/<int:tp_id>', tp.delete_tp,
         name="delete-tp"),
    path('managed/promotion/<int:promotion_id>/delete/subject/<int:subject_id>', subject.delete_subject,
         name="delete-subject"),
    path('managed/promotion/<int:promotion_id>/managed/subject/<int:subject_id>/delete/session/<int:session_id>',
         session.delete_session, name="delete-session"),

    path('managed/year/<int:year_id>/delete/planning/<int:planning_id>', planning.delete_planning,
         name='delete-planning'),
]
