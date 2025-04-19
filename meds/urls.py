from django.urls import path
from . import views

app_name = 'meds'

urlpatterns = [
    path('', views.home, name='home'),
    path('medications/', views.list_medications, name='list_medications'),
    path('medications/<int:med_id>/dispense/', views.dispense_form, name='dispense_form'),
]
