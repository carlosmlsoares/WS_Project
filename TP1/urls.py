from django.urls import path
from TP1 import views

urlpatterns = [
    path('', views.index, name="index"),
    path('movies/', views.movies, name="movies"),
    path('movie/(?P<id>[^/]+)$', views.movie, name="movie"),
    path('actors/', views.actors, name="actors"),
    path('actor/(?P<id>[^/]+)$', views.actor, name="actor"),
    path('directors/', views.directors, name="directors"),
    path('director/(?P<id>[^/]+)$', views.directors, name="director"),
    path('genre/<id>', views.genre, name="genre")
]
