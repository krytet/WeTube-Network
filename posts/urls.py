from django.urls import path

from . import views

urlpatterns = [
    # главная страница проекта
    path("", views.index, name="index"),
    # Страница создания новых постов
    path("new/", views.new_post, name="new_post"),
    # новые записи подписок
    path("follow/", views.follow_index, name='follow_index'),
    # Профайл пользователя
    path('<str:username>/', views.profile, name='profile'),
    # Просмотр записи
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    # Редактирование записи
    path(
        '<str:username>/<int:post_id>/edit/', 
        views.post_edit, 
        name='post_edit'
    ),
    # Подписаться на пользователя
    path("<str:username>/follow/", views.profile_follow, name="profile_follow"), 
    # Отписаться от пользователя
    path("<str:username>/unfollow/", views.profile_unfollow, name="profile_unfollow"),
    # написание коментов
    path("<username>/<int:post_id>/comment", views.add_comment, name="add_comment"),

]