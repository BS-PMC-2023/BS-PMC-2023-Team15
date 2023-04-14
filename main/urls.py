
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import main.views

urlpatterns = [
    # path('/item/', admin.site.urls),
    path('<category>', main.views.category_view, name='item'),
    path('details/', main.views.item_view, name='details'),
    path('reserve/', main.views.reserve_item, name='reserve_item'),
]
