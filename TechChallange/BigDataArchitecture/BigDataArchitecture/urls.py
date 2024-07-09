from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('process/', views.download_and_process, name='download_and_process'),
    path('view/', views.view, name = 'view'),
]
