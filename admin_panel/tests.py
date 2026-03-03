from django.test import TestCase, Client
from django.urls import reverse

# basic smoke tests for the newly added feedback "featured" feature
from .models import Feedback

class FeedbackFeatureTests(TestCase):
	def setUp(self):
		self.client = Client()
		# create a sample feedback entry
		self.feedback = Feedback.objects.create(
			name='Tester',
			email='tester@example.com',
			mobile_number='9999999999',
			rating=4,
			feedback='Sample feedback'
		)

	def test_toggle_featured_view(self):
		# toggling should flip the boolean and redirect back
		url = reverse('feedback:toggle_featured_feedback', args=[self.feedback.id])
		resp = self.client.post(url)
		self.feedback.refresh_from_db()
		self.assertTrue(self.feedback.featured)
		# second POST should unset
		resp = self.client.post(url)
		self.feedback.refresh_from_db()
		self.assertFalse(self.feedback.featured)

	def test_homepage_includes_featured_feedback(self):
		# mark as featured and load the index page
		self.feedback.featured = True
		self.feedback.save()
		resp = self.client.get(reverse('user_panel:index'))
		self.assertEqual(resp.status_code, 200)
		# testimonial heading should appear
		self.assertContains(resp, 'Hear <i>from them</i>')
		# feedback text must appear
		self.assertContains(resp, 'Sample feedback')

