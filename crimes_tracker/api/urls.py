from django.urls import path
from .views import Index

urlpatterns = [
    path("", Index.as_view(), name="index"),
]
# Compare this snippet from crimes_tracker/api/models.py: