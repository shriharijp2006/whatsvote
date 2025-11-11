from django.urls import path
from . import views

urlpatterns = [
    path("", views.poll_list, name="poll_list"),
    path("poll/<int:pk>/", views.poll_detail, name="poll_detail"),
    path("create/", views.create_poll, name="create_poll"),
]
