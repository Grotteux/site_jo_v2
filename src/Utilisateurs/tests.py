from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from Utilisateurs.models import KeyUser
from Utilisateurs.forms import CustomSignupForm
from unittest.mock import patch

User = get_user_model()

class UtilisateursViewsTests(TestCase):
    def test_cgu_view(self):
        response = self.client.get(reverse('cgu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cgu.html')

    def test_account_profile_view(self):
        response = self.client.get(reverse('account_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_profile.html')
class KeyUserModelTests(TestCase):
    def test_key_user_creation(self):
        user = User.objects.create_user(username="testuser", password="password")
        self.assertTrue(KeyUser.objects.filter(user=user).exists())
        key_user = KeyUser.objects.get(user=user)
        self.assertIsNotNone(key_user.user_key)

class CustomSignupFormTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_custom_signup_form(self):
        form_data = {
            "email": "test@example.com",
            "password1": "complexpassword123",
            "password2": "complexpassword123",
            "first_name": "John",
            "last_name": "Doe"
        }
        form = CustomSignupForm(data=form_data)
        self.assertTrue(form.is_valid())
        request = self.factory.post("/signup/", form_data)
        request.session = self.client.session
        user = form.save(request)
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")

class ViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    @patch('Ticket.decorators.user_has_device', return_value=True)
    def test_ticket_list_view_with_2fa(self, mock_user_has_device):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse('ticket_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Choisissez vos tickets")

    @patch('Ticket.decorators.user_has_device', return_value=False)
    def test_ticket_list_view_redirect_to_2fa(self, mock_user_has_device):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse('ticket_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('two-factor-setup'))

    def test_ticket_list_redirect_if_not_authenticated(self):
        response = self.client.get(reverse('ticket_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account_login'))
