# filepath: psnapp/urls.py
from django.contrib import admin
from django.urls import path
from psnapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.psn_form, name='psn_form'),
    path('success/', views.success, name='success'),
    path('thank_you/', views.thank_you, name='thank_you'),
    path('download/', views.download_psn_entries, name='download_psn_entries'),
    path('approve_request/<int:id>/', views.approve_request, name='approve_request'),
    path('reject_request/<int:id>/', views.reject_request, name='reject_request'),
    path('approve_hod_request/<int:id>/', views.approve_hod_request, name='approve_hod_request'),
    path('reject_hod_request/<int:id>/', views.reject_hod_request, name='reject_hod_request'),
    path('engineer_response/<int:id>/', views.engineer_response, name='engineer_response'),
    path('request_details/<int:id>/', views.request_details, name='request_details'),
    path('psn_form/', views.psn_form, name='psn_form'),
    path('download_data/', views.download_data, name='download_data'),
]
