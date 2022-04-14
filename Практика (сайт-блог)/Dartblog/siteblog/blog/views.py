from msilib import CAB
from unicodedata import category
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .models import *

class Home(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Classic Blog Design'
        return context


class PostByCategory(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 2
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context



# def index(request):
#     posts = Post.objects.all()
#     paginator = Paginator(posts, 2)

#     page_number = request.GET.get('page', 1)
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'blog/index.html', {'page_obj': page_obj, 'title': 'Classic Blog Design'})


def get_category(request, slug):
    return render(request, 'blog/category.html')

def get_post(request, slug):
    return render(request, 'blog/post.html')