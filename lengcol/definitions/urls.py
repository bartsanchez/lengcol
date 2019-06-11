from django.urls import path
from definitions import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('definitions/add/',
         views.DefinitionCreateView.as_view(),
         name='definition-add'),

    path('definitions/<int:pk>/',
         views.DefinitionDetailView.as_view(),
         name='definition-detail'),

    path('terms/<str:slug>/',
         views.TermDetailView.as_view(),
         name='term-detail'),
]
