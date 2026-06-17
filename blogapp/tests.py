# pyrefly: ignore [missing-import]
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import NewsletterSubscription

# Create your tests here.
class NewsletterSubscriptionTests(APITestCase):
    def test_subscribe_newsletter_success(self):
        url = reverse("subscribe_newsletter")
        data = {"email": "test@example.com"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Subscribed successfully", response.data["message"])
        self.assertTrue(NewsletterSubscription.objects.filter(email="test@example.com").exists())

    def test_subscribe_newsletter_duplicate(self):
        # Create an existing subscription
        NewsletterSubscription.objects.create(email="test@example.com")
        url = reverse("subscribe_newsletter")
        data = {"email": "test@example.com"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "This email is already subscribed.")

    def test_subscribe_newsletter_invalid_email(self):
        url = reverse("subscribe_newsletter")
        data = {"email": "not-an-email"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

