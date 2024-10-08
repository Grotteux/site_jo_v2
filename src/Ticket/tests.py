from django.test import TestCase
from django.urls import reverse
from .models import Ticket, TicketType, Purchase
from django.contrib.auth.models import User
from unittest.mock import patch


class TicketTestCase(TestCase):

    @patch('Ticket.decorators.two_factor_required', lambda x: x)
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.admin_user = User.objects.create_user(username='adminuser', password='adminpass', is_staff=True)
        self.ticket_type_solo = TicketType.objects.create(name='Solo')
        self.ticket_type_duo = TicketType.objects.create(name='Duo')
        self.ticket_solo = Ticket.objects.create(type=self.ticket_type_solo, price=50)
        self.ticket_duo = Ticket.objects.create(type=self.ticket_type_duo, price=90)

    def test_ticket_creation(self):
        self.assertEqual(Ticket.objects.count(), 2)
        self.assertEqual(self.ticket_solo.price, 50)
        self.assertEqual(self.ticket_duo.price, 90)

    def test_purchase(self):
        self.client.login(username='testuser', password='testpass')
        purchase = Purchase.objects.create(ticket=self.ticket_solo, user=self.user)
        self.assertEqual(Purchase.objects.count(), 1)

    @patch('Ticket.decorators.user_has_device',return_value=True)
    def test_ticket_page_access(self, mock_user_has_device):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('ticket_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Choisissez vos tickets')

    def test_admin_dashboard_access(self):
        self.client.login(username='adminuser', password='adminpass')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Administration - Nombre de billets vendus')

    def test_validate_qr_access(self):
        self.client.login(username='adminuser', password='adminpass')
        response = self.client.get(reverse('validate_qr'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Scan QR CODE')

    def test_get_qr_data(self):
        purchase = Purchase.objects.create(ticket=self.ticket_solo, user=self.user)
        qr_data = purchase.get_qr_data()
        self.assertIn(str(self.user.keyuser.user_key), qr_data)
        self.assertIn(str(purchase.unique_key), qr_data)

    def test_two_factor_required_redirect(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('ticket_list'))
        self.assertEqual(response.status_code, 302)  # Devrait rediriger vers le setup du 2FA
        self.assertRedirects(response, '/accounts/setup/')

    def test_process_purchase(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'tickets': [
                {'id': self.ticket_solo.id, 'quantity': 1},
                {'id': self.ticket_duo.id, 'quantity': 2},
            ]
        }
        response = self.client.post(reverse('process_purchase'), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Purchase.objects.count(), 3)


