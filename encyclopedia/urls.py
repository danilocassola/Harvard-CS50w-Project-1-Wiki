from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.title, name="title"),
    path("new", views.newpage, name="newpage"),
    path("edit", views.edit, name="edit"),
    path("update", views.update, name="update"),
    path("randompage", views.randompage, name="randompage"),
    path("search", views.search, name="search")
]