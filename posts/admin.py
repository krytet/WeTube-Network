from django.contrib import admin

from .models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    #свойства модели для отображения
    list_display = ("pk","text", "pub_date", "author") 
    # поиск по
    search_fields = ("text",)
    # возможность фильтрации по
    list_filter = ("pub_date",) 
    empty_value_display = "-пусто-"



admin.site.register(Post, PostAdmin)

