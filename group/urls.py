from django.urls import path

from . import views

urlpatterns = [
    path("<slug:slug>/", views.group_post, name='group'),
]