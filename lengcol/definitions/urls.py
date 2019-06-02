from django.urls import path
from definitions import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('definitions/add/', views.DefinitionCreateView.as_view(), name='add'),
    path('definitions/<int:pk>/',
         views.DefinitionDetailView.as_view(),
         name='detail'),
]
