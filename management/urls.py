from django.urls import path

from . import views

app_name = 'management'
urlpatterns = [
  path('', views.index, name='index'),
  path('/add/year', views.addYear, name="add-year"),
  path('/add/teacher', views.addTeacher, name="add-teacher"),
  path('/add/promotion', views.addPromotion, name="add-promotion"),


  path('/edit/promotion/<int:promotion_id>', views.editPromotion, name="edit-promotion"),
  
  path('/edit/promotion/<int:promotion_id>/add/td', views.addTd, name="add-td"),
  path('/edit/promotion/<int:promotion_id>/edit/td/<int:td_id>', views.editTd, name="edit-td"),
  path('/edit/promotion/<int:promotion_id>/edit/td/<int:td_id>/add/tp', views.addTp, name="add-tp"),
  
  path('/edit/promotion/<int:promotion_id>/add/subject', views.addSubject, name="add-subject"),
  path('/edit/promotion/<int:promotion_id>/edit/subject/<int:subject_id>', views.editSubject, name="edit-subject"),
  path('/edit/promotion/<int:promotion_id>/edit/subject/<int:subject_id>/add/session/cm', views.addCmSession, name="add-cm-session"),
  path('/edit/promotion/<int:promotion_id>/edit/subject/<int:subject_id>/add/session/td', views.addTdSession, name="add-td-session"),
  path('/edit/promotion/<int:promotion_id>/edit/subject/<int:subject_id>/add/session/tp', views.addTpSession, name="add-tp-session"),

  path('/edit/year/<int:year_id>', views.editYear, name="edit-year"),
]