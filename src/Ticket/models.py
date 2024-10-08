from django.contrib.auth import get_user_model
from django.db import models
import uuid

User = get_user_model()

class TicketType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.type} - {self.price}€"

class Purchase(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    unique_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Achat de {self.ticket} par {self.user} - Clé : {self.unique_key}"

    def get_qr_data(self):
        # Concaténer la clé utilisateur et la clé du billet
        return f"{self.user.keyuser.user_key}_{self.unique_key}"
