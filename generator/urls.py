from django.urls import path
from . import views

urlpatterns = [
    path('checks/', views.checks),
    path('checks/create/', views.create_checks),#need api_key param
    path('checks/pdf/', views.get_check_pdf),#need api_key and check_id params
]