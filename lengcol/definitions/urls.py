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

    path('definitions/<uuid:uuid>/change',
         views.DefinitionUpdateView.as_view(),
         name='definition-update'),

    path('definitions/<uuid:uuid>/disable',
         views.DefinitionDisableView.as_view(),
         name='definition-disable'),

    path('terms/search/',
         views.TermSearchView.as_view(),
         name='term-search'),

    path('terms/<slug:slug>/',
         views.TermDetailView.as_view(),
         name='term-detail'),

    path('tags/',
         views.TagListView.as_view(),
         name='tag-list'),

    path('tags/<str:tag_name>/definitions/',
         views.DefinitionsByTagView.as_view(),
         name='definitions-by-tag'),
]
