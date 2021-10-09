from django.shortcuts import render
#  функция reverse_lazy позволяет получить URL по параметру "name" функции path()
#  берём, тоже пригодится
from django.urls import reverse_lazy
#  импортируем CreateView, чтобы создать ему наследника
from django.views.generic import CreateView

#  импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login")
    template_name = 'signup.html'

# Create your views here.
