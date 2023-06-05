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


urlpatterns = [
    path('admin', admin.site.urls),
    path('', main.views.main_view, name='main'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('accounts/logout', accounts.views.logout_view, name='logout'),
    path('malfunction/<serial>', main.views.malfunction_view, name='malfunction'),
    path('report', main.views.mal_view, name='mal'),
    path('categories', main.views.categories_view, name='categories'),
    path('categories/studio', main.views.studio_view, name='studio'),
    path('personal_profile/<student>', main.views.personal_profile, name='personal'),
    path('categories/podcast', main.views.podcast_view, name='podcast'),
    path('category/', include('main.urls'), name='category'),
    path('requests', main.views.requests, name='requests'),
    path('overdue', main.views.overdue, name='overdue'),
    path('statistics', main.views.stats, name='stats'),
    path('history/<user>', main.views.history, name='history'),
    path('myhistory/<user>', main.views.myhistory, name='myhistory'),
    path('search', main.views.search, name='search'),
    path('profile/<item>/return', main.views.profile_return, name='return'),
    path('profile/view', main.views.profile_view, name='profile'),
    path('policy', main.views.policy_view, name='policy'),
    path('addstudents', main.views.addstudents, name='addstudents'),
    path('pass/<item>', main.views.pass_item_view_new, name='pass'),
    path('pass/<item>', main.views.pass_item_to_student, name='pass_confirm'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)