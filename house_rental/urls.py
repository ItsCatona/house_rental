from django.contrib import admin
from django.urls import path, include
from rental_system import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('rental_system.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
