from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import main.views


urlpatterns = [

    # path('/item/', admin.site.urls),
    path('<category>', main.views.category_view, name='category'),
    path('details/<item>', main.views.item_detail_view, name='details'),


]
