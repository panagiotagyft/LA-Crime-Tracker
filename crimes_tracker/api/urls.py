from django.urls import path
from .views import Index, get_users, add_user

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("users/", get_users, name="get_users"),
    path("users/add_user", add_user, name="add_user"),
]