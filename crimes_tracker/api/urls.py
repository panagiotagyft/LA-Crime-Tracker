from django.urls import path
from .views import Index, get_users, add_user
from .views import reports_per_crime_code_in_time_range

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("users/", get_users, name="get_users"),
    path("users/add_user", add_user, name="add_user"),
    path('reports_per_crime_code/', reports_per_crime_code_in_time_range, name='reports_per_crime_code'),
]