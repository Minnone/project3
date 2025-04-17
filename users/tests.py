from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date

class AdminHackTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='admin@mirea.ru',
            email='admin@mirea.ru',
            password='adminpass123',
            is_staff=True
        )
        self.client.login(username='admin@mirea.ru', password='adminpass123')
        self.admin_hack_url = reverse('users:admin_hack')

    def test_add_hackathon_modal(self):
        """Test the add hackathon modal functionality"""
        response = self.client.get(self.admin_hack_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'addHackathonModal')  # Check modal exists in HTML
        self.assertContains(response, 'class="hackinfo-right-button"')  # Check add button exists
        self.assertContains(response, 'id="addHackathonForm"')  # Check form exists

    def test_modal_visibility_css(self):
        """Test that modal CSS is properly configured"""
        response = self.client.get(self.admin_hack_url)
        self.assertContains(response, 'adminHack.css')
        # We can't directly test CSS rules in Django tests, but we can verify the CSS file is included