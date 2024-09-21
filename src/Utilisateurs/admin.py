from django.contrib import admin

from Utilisateurs.models import KeyUser


# Register your models here.
class UtilisateursKeyAdmin(admin.ModelAdmin):
    list_display = ("user", "user_key", "created_at")

admin.site.register(KeyUser, UtilisateursKeyAdmin)