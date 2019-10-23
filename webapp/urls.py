from django.contrib import admin
from django.urls import path

from hash.views import home_view, hash_url, quickhash

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='homepage'),
    path('sha256/<str:sha256>/', hash_url, name='hashpage'),
    path('quickhash/', quickhash, name='quickhashpage'),
]
