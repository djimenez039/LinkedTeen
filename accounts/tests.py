from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthFlowTests(TestCase):
    def test_login_page_loads(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log in')

    def test_register_page_loads(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create an account')

    def test_login_redirects_to_dashboard(self):
        user = get_user_model().objects.create_user(username='demo', password='StrongPass123!')
        response = self.client.post(reverse('accounts:login'), {
            'username': 'demo',
            'password': 'StrongPass123!',
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_register_redirects_to_onboarding(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertRedirects(response, reverse('accounts:onboarding'))
        self.assertTrue(get_user_model().objects.filter(username='newuser').exists())

    def test_student_onboarding_page_loads_for_logged_in_user(self):
        user = get_user_model().objects.create_user(username='profileuser', password='StrongPass123!')
        self.client.login(username='profileuser', password='StrongPass123!')
        response = self.client.get(reverse('accounts:onboarding'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'What I can offer')
        self.assertContains(response, 'I am looking for')

    def test_profile_page_loads_for_logged_in_user(self):
        user = get_user_model().objects.create_user(username='profileviewer', password='StrongPass123!')
        self.client.login(username='profileviewer', password='StrongPass123!')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Student profile')

    def test_logout_returns_to_home(self):
        user = get_user_model().objects.create_user(username='logoutuser', password='StrongPass123!')
        self.client.login(username='logoutuser', password='StrongPass123!')
        response = self.client.post(reverse('accounts:logout'))
        self.assertRedirects(response, reverse('home'))
        self.assertNotIn('_auth_user_id', self.client.session)
