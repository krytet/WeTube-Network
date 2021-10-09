from django.contrib import admin

from .models import Group

# Register your models here.

class GroupAdmin(admin.ModelAdmin):
    #свойства модели для отображения
    list_display = ("pk","title", "slug", "description") 
    # поиск по
    search_fields = ("title",)

    empty_value_display = "-пусто-"



admin.site.register(Group, GroupAdmin)