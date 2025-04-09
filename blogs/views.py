from django.shortcuts import render
from .models import BlogSettings, Pages
from django.shortcuts import render, get_object_or_404


def index(request):
    blogsettings = BlogSettings.objects.first()
    pages = Pages.objects.all()
    context = {
        'blogsettings': blogsettings,
        'pages': pages
    }
    return render(request, 'blogs/blogs.html', context)


def blog_page_view(request, slug):
    page = get_object_or_404(Pages, slug=slug)
    context = {
        'page': page,
    }
    return render(request, 'blogs/blog-pages.html', context)
