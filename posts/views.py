from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .forms import CommentForm, PostForm
from .models import Follow, Post

User = get_user_model()

# Create your views here.
@cache_page(20)
def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10) # показывать по 10 записей на странице.
    page_number = request.GET.get('page') # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number) # получить записи с нужным смещением
    context = {
        'page': page,
        'paginator': paginator
    }
    return render(request, 'index.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    following = (request.user.is_authenticated and Follow.objects.filter(
        author=author, user=request.user).exists())
    posts = Post.objects.filter(author=author).order_by("-pub_date").all()
    posts_count = posts.count()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    # тут тело функции
    context = {
        'page' : page,
        'paginator' : paginator,
        'profile' : author,
        'posts_count' : posts_count,
        'following' : following,
    }
    return render(request, 'post/profile.html', context)


def post_view(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    posts_count = post.author.posts.count()
    form = CommentForm()
    comments = post.comments.all()
    # тут тело функции
    context = {
        'post' : post,
        'posts_count' : posts_count,
        'form' : form,
        'comments' : comments,
    }
    return render(request, 'post/post_view.html', context)


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    if post.author != request.user:
        return redirect('post', username=username, post_id=post_id)
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('post', username=username, post_id=post_id)
        # тут тело функции. Не забудьте проверить, 
        # что текущий пользователь — это автор записи.
        # В качестве шаблона страницы редактирования укажите шаблон создания новой записи
        # который вы создали раньше (вы могли назвать шаблон иначе)
    context = {
        'form' : form,
        'is_edit' : True,
        'post' : post,
    }
    return render(request, 'post/new_post.html', context)


@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST' and form.is_valid:
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('index')
    return render(request, 'post/new_post.html', {'form' : form, 'is_edit' : False})


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    form = CommentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid:
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('post', username=username, post_id=post_id)


@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user).order_by("-pub_date")
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page' : page,
        'paginator' : paginator,
    }
    return render(request, 'post/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(author=author, user=request.user)
    return redirect('profile', username=username)



@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(author=author, user=request.user).delete()
    return redirect('profile', username=username)


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию, 
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(
        request, 
        "misc/404.html", 
        {"path" : request.path}, 
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
