"""CreativeStorage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from HomePage.views import login_view, student_view, malfunction_view, lecturer_view, manager_view, podcast_view, \
    products_view, studio_view, profile_view, contact_view

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', login_view, name='Home'),
    path('HomeS', student_view, name='HomeS'),
    path('HomeL', lecturer_view, name='HomeL'),
    path('HomeM', manager_view, name='HomeM'),
    path('malfunctions', malfunction_view, name='malfunctions'),
    path('products', products_view, name='products'),
    path('studio', studio_view, name='studio'),
    path('podcast', podcast_view, name='podcast'),
    path('profile', profile_view, name='profile'),
    path('contact', contact_view, name='contact'),
]
