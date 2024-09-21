from django.contrib import admin
from django.urls import path, include
from Ticket.views import ticket_list, process_purchase, my_tickets, validate_qr, admin_dashboard
from Utilisateurs.views import cgu, account_profile
from site_jo.views import vue_principal, vue_contact, vue_billet_connect

urlpatterns = [
    path("admin/", admin.site.urls, name='admin'),
    path("moncompte/", account_profile, name='account_profile'),
    path("", vue_principal, name='home'),
    path("contact/", vue_contact, name='contact'),
    path("signup/", include("allauth.urls")),  # Allauth signup, login, etc.
    path("profile/", include("allauth.urls")),  # Profile-related routes
    path('tickets/', ticket_list, name='ticket_list'),
    path('process_purchase/', process_purchase, name='process_purchase'),
    path('mes-billets/', my_tickets, name='my_tickets'),
    path('cgu/', cgu, name='cgu'),
    path('billets/', vue_billet_connect, name='billet'),
    path('employee/validate/', validate_qr, name='validate_qr'),
    path('accounts/', include('allauth_2fa.urls')),
    path('accounts/', include('allauth.urls')),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
]
