from django.urls import path
from .views.queries_views.query1_views import Query1View
from .views.queries_views.query2_views import Query2View
from .views.queries_views.query3_views import Query3View
from .views.queries_views.query4_views import Query4View
from .views.queries_views.query5_views import Query5View
from .views.queries_views.query6_views import Query6View

from .views.functions_views import DropdownOptionsView, GetCodeDescriptionView, GenerateDRNOView, GetRecordByDRNOView
from .views.insert_views import InsertView
from .views.update_views import UpdateView

urlpatterns = [
    # queries
    path('query1/', Query1View.as_view(), name='query1'),
    path('query2/', Query2View.as_view(), name='query2'),
    path('query3/', Query3View.as_view(), name='query3'),
    path('query4/', Query4View.as_view(), name='query4'),
    path('query5/', Query5View.as_view(), name='query5'),
    path('query6/', Query6View.as_view(), name='query6'),

    # functions
    path('dropdown-options/', DropdownOptionsView.as_view(), name='dropdown-options'),
    path('get-code-description/', GetCodeDescriptionView.as_view(), name='get-code-description'),
    path('generate-drno/', GenerateDRNOView.as_view(), name='generate-drno'),
    path('get-record/', GetRecordByDRNOView.as_view(), name='get-record'),

    # updates & insert
    path('insert-record/', InsertView.as_view(), name='insert-record'),
    path('update-record/', UpdateView.as_view(), name='update-record'),
]
