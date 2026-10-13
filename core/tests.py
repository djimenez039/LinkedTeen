from django.test import TestCase
from django.urls import reverse

from clubs.models import Club


class PublicPagesTests(TestCase):
	def test_homepage_shows_live_club_count_and_policy_links(self):
		Club.objects.create(name='Test Club')

		response = self.client.get(reverse('home'))

		self.assertContains(response, '1 clubs to explore')
		self.assertContains(response, reverse('terms'))
		self.assertContains(response, reverse('privacy'))
		self.assertContains(response, 'Ponte Vedra High School students only.')
		self.assertContains(response, 'Username and password are required; email and profile photo are optional.')
		self.assertEqual(response.content.decode().count('Ponte Vedra High School students only'), 1)
		self.assertEqual(response.content.decode().count('By registering, you agree to our'), 0)

	def test_terms_and_privacy_pages_are_public(self):
		terms_response = self.client.get(reverse('terms'))
		privacy_response = self.client.get(reverse('privacy'))

		self.assertContains(terms_response, 'LinkedTeens Terms of Use')
		self.assertContains(privacy_response, 'LinkedTeens Privacy Policy')

	def test_registration_page_links_to_terms_and_privacy(self):
		response = self.client.get(reverse('accounts:register'))

		self.assertContains(response, reverse('terms'))
		self.assertContains(response, reverse('privacy'))
