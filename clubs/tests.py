from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Club, ClubAnnouncement, ClubMembership, ClubPost


class ClubMembershipAndAnnouncementTests(TestCase):
	def setUp(self):
		self.club = Club.objects.create(name='Test Club', description='A test club.')
		self.student = get_user_model().objects.create_user(username='student', password='StrongPass123!')
		self.club_url = reverse('club_detail', args=[self.club.pk])

	def test_join_immediately_creates_one_membership(self):
		self.client.login(username='student', password='StrongPass123!')
		join_url = reverse('join_club', args=[self.club.pk])

		self.client.post(join_url)
		self.client.post(join_url)

		self.assertEqual(ClubMembership.objects.filter(club=self.club, student=self.student).count(), 1)
		self.assertEqual(ClubMembership.objects.get(club=self.club, student=self.student).role, 'member')

	def test_announcement_is_public_but_member_cannot_publish(self):
		announcement = ClubAnnouncement.objects.create(
			club=self.club,
			author=self.student,
			title='Meeting update',
			body='The meeting is Thursday.',
		)
		self.client.login(username='student', password='StrongPass123!')
		ClubMembership.objects.create(club=self.club, student=self.student)

		response = self.client.get(self.club_url)

		self.assertContains(response, announcement.title)
		self.assertEqual(
			self.client.post(reverse('create_club_announcement', args=[self.club.pk]), {
				'title': 'Member announcement',
				'body': 'This should be rejected.',
			}).status_code,
			403,
		)
		self.assertFalse(ClubAnnouncement.objects.filter(title='Member announcement').exists())

	def test_designated_leader_can_publish_public_announcement(self):
		ClubMembership.objects.create(club=self.club, student=self.student, role='leader')
		self.client.login(username='student', password='StrongPass123!')

		response = self.client.post(reverse('create_club_announcement', args=[self.club.pk]), {
			'title': 'Club meeting',
			'body': 'Meet after school.',
		})

		self.assertRedirects(response, self.club_url)
		self.assertTrue(ClubAnnouncement.objects.filter(club=self.club, title='Club meeting').exists())
		self.client.logout()
		self.assertContains(self.client.get(self.club_url), 'Meet after school.')

	def test_only_members_can_view_and_create_group_posts(self):
		ClubPost.objects.create(club=self.club, author=self.student, body='Member discussion')

		self.assertNotContains(self.client.get(self.club_url), 'Member discussion')

		ClubMembership.objects.create(club=self.club, student=self.student)
		self.client.login(username='student', password='StrongPass123!')
		self.assertContains(self.client.get(self.club_url), 'Member discussion')
		self.client.post(reverse('create_club_post', args=[self.club.pk]), {'body': 'Another discussion'})
		self.assertTrue(ClubPost.objects.filter(club=self.club, body='Another discussion').exists())
