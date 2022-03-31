from unicodedata import name
from django.urls import path
from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<title>", views.entry, name="entry"),
    path("search", views.search, name="searched"),
    path("create", views.create, name="create"),
    path("<title>/edit", views.edit, name="edit"),
    path("random", views.random_page, name="random")
]
