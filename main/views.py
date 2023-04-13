from django.shortcuts import render
from database.models import Category, Equipment
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


def category_view(request, category):
    # category = Category.objects.get(name=category)
    items = Equipment.objects.filter(category=category)
    return render(request, 'catalog.html', {"items":items})


def item_view(request, category, item, item_brand, item_model, item_description, item_image, item_price, item_quantity, item_category):
    item = Equipment.objects.get(name=item)

    return render(request, 'item.html', {"item_brand":item_brand, "item_model":item_model, "item_description":item_description, "item_image":item_image, "item_price":item_price, "item_quantity":item_quantity, "item_category":item_category, "item":item})
