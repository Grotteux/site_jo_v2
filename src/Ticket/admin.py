from django.contrib import admin
from .models import Ticket, Purchase, TicketType


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('type', 'price')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'purchase_date', 'unique_key')

@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)