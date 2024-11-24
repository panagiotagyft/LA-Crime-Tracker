from django.urls import path
from .views import Query1View, DropdownOptionsView, GetCodeDescriptionView, GenerateDRNOView, SaveNewCodeView

urlpatterns = [
    path('query1/', Query1View.as_view(), name='query1'),
    path('dropdown-options/', DropdownOptionsView.as_view(), name='dropdown-options'),
    path('get-code-description/', GetCodeDescriptionView.as_view(), name='get-code-description'),
    path('generate-drno/', GenerateDRNOView.as_view(), name='generate-drno'),
    path('save-new-code/', SaveNewCodeView.as_view(), name='save-new-code'),
]
