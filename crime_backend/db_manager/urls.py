from django.urls import path
from .views import Query1View

urlpatterns = [
    path('query1/', Query1View.as_view(), name='query1'),
]
