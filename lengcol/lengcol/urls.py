from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('definitions.urls')),
    path('', include('authentication.urls')),
    path('admin/', admin.site.urls),
]
