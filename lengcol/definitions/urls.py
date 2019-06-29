from django.urls import path
from definitions import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('definitions/add/',
         views.DefinitionCreateView.as_view(),
         name='definition-add'),

    path('definitions/<uuid:uuid>/',
         views.DefinitionDetailView.as_view(),
         name='definition-detail'),

    path('terms/search/<str:term>',
         views.TermSearchView.as_view(),
         name='term-search'),

    path('terms/<slug:slug>/',
         views.TermDetailView.as_view(),
         name='term-detail'),
]
