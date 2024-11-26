from django.urls import path
from .views.queries_views.query1_views import Query1View
from .views.queries_views.query2_views import Query2View
from .views.functions_views import DropdownOptionsView, GetCodeDescriptionView, GenerateDRNOView, GetRecordByDRNOView
from .views.insert_views import InsertView
from .views.update_views import UpdateView

urlpatterns = [
    # queries
    path('query1/', Query1View.as_view(), name='query1'),
    path('query2/', Query2View.as_view(), name='query2'),
    
    # functions
    path('dropdown-options/', DropdownOptionsView.as_view(), name='dropdown-options'),
    path('get-code-description/', GetCodeDescriptionView.as_view(), name='get-code-description'),
    path('generate-drno/', GenerateDRNOView.as_view(), name='generate-drno'),
    path('get-record/', GetRecordByDRNOView.as_view(), name='get-record'),

    # updates & insert
    path('insert-record/', InsertView.as_view(), name='insert-record'),
    path('update-record/', UpdateView.as_view(), name='update-record'),
]
