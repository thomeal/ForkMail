from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/', views.register),
    url(r'^login/', views.login),
    url(r'^getAllMails/', views.getMails),
    url(r'^getMailBoxes/', views.getMailBoxes),
    url(r'^addMailBox/', views.addMailBox),
    url(r'^deleteMailBox/', views.deleteMailBox),
    url(r'^editMailBox/', views.editMailBox),
    url(r'^deleteMail/', views.deleteMail),
    url(r'^sendMail/', views.sendMail),
]
