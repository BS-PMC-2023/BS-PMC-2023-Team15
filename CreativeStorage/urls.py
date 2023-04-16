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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import core.views
import accounts.views
import main.views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main.views.main_view, name='main'),
    # path('lecturer', apps.pages.views.lecturer_view, name='lecturer'),
    # path('manager', apps.pages.views.manager_view, name='manager'),
    path('malfunction', main.views.malfunction_view, name='malfunction'),
    path('products', main.views.product_view, name='products'),
    path('studio', main.views.studio_view, name='studio'),
    path('podcast', main.views.podcast_view, name='podcast'),
    path('category/', include('main.urls'), name='category'),
    # path('contact', apps.pages.views.contact_view, name='contact'),
    # path('login', login.views.login_view, name='login'),
    # path('profile', apps.pages.views.profile_view, name='profile'),
    path("accounts/", include("django.contrib.auth.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)