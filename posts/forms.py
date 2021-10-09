from django.db.models import fields
from django.forms import ModelForm

from .models import Comment, Post


#  создадим собственный класс для формы регистрации
#  сделаем его наследником предустановленного класса UserCreationForm
class PostForm(ModelForm):
    #  наследуется класс Meta, вложенный в класс UserCreationForm:
    class Meta():
        # укажем модель, с которой связана создаваемая форма
        model = Post
        # укажем, какие поля должны быть видны в форме и в каком порядке
        fields = ['group', 'text','image']


class CommentForm(ModelForm):
    class Meta():
        model = Comment
        fields = ['text']