from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DashboardViewTests(TestCase):
    def test_dashboard_page_loads(self):
        user = get_user_model().objects.create_user(username='dashboarduser', password='StrongPass123!')
        self.client.login(username='dashboarduser', password='StrongPass123!')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Connection engine')
        self.assertContains(response, 'What you can offer')

    def test_clubs_page_loads(self):
        response = self.client.get(reverse('clubs'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Where your skills are needed')

    def test_opportunities_page_loads(self):
        response = self.client.get(reverse('opportunities'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Opportunities that fit your goals')
