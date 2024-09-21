from django.contrib import admin
from .models import Ticket, Purchase

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('type', 'price')
    list_editable = ('price',)

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'purchase_date', 'unique_key')
