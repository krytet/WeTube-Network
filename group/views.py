from django.core import paginator
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from posts.models import Post

from .models import Group


# Create your views here.
def group_post(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'group': group,
        'page' : page,
        'paginator' : paginator
    }
    return render(request, 'group.html',context)