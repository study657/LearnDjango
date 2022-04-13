from django.core.paginator import Paginator
from django.shortcuts import render
from .models import *

def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 2)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/index.html', {'page_obj': page_obj, 'title': 'Classic Blog Design'})


def get_category(request, slug):
    return render(request, 'blog/category.html')

def get_post(request, slug):
    return render(request, 'blog/post.html')