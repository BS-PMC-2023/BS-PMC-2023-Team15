from django.shortcuts import render
from database.models import Category
# Create your views here.

def main_view(request):
    return render(request, 'categories.html', {} )


def product_view(request):
    categories = Category.objects.all()
    return render(request, 'products.html', {'categories': categories})


def studio_view(request):
    return render(request, 'studio.html', {})


def podcast_view(request):
    return render(request, 'podcast.html', {})

def malfunction_view(request):
    return render(request, 'malfunction.html', {})