from django.urls import path
from TP1 import views

urlpatterns = [
    path('', views.index, name="index"),
    path('movies/', views.movies, name="movies"),
    path('movie/<id>', views.movie, name="movie"),
    path('actors/', views.actors, name="actors"),
    path('actor/<id>', views.actor, name="actor"),
    path('directors/', views.directors, name="directors"),
    path('director/<id>', views.director, name="director"),
    path('genre/<id>', views.genre, name="genre"),
    path('search/', views.search, name="search"),
    path('inferences/', views.inferences, name="inferences"),
    path('inferences/<id>', views.exec_inferences, name="exec_inferences")
]
