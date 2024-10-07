from django.test import TestCase
from django.urls import reverse
from .models import Ticket, TicketType, Purchase
from django.contrib.auth.models import User

class TicketTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Créer des types de tickets
        self.ticket_type_solo = TicketType.objects.create(name='Solo')
        self.ticket_type_duo = TicketType.objects.create(name='Duo')

        # Créer des billets en utilisant les types de tickets
        self.ticket_solo = Ticket.objects.create(type=self.ticket_type_solo, price=50)
        self.ticket_duo = Ticket.objects.create(type=self.ticket_type_duo, price=90)

    def test_ticket_creation(self):
        self.assertEqual(Ticket.objects.count(), 2)
        self.assertEqual(self.ticket_solo.price, 50)
        self.assertEqual(self.ticket_duo.price, 90)

    def test_purchase(self):
        # Simuler un achat de billet
        self.client.login(username='testuser', password='testpass')
        purchase = Purchase.objects.create(ticket=self.ticket_solo, user=self.user)
        self.assertEqual(Purchase.objects.count(), 1)

    def test_ticket_page_access(self):
        response = self.client.get(reverse('ticket_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Choisissez vos tickets')
