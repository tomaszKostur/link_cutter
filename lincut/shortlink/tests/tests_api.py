from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from shortlink.views import REDIRECT_PATH

from shortlink.models import LinkMap


class LinkMapApiTests(APITestCase):

    def test_create_short_link(self):
        response = self.client.post(
            "/linkmap/", {"orig_url": "https://foobarbaz.com"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(set(response.data.keys()), {"short_url"})
        print(f"DEVDEV {response.data["short_url"]}")
        self.assertTrue(REDIRECT_PATH in response.data["short_url"])

    @patch("shortlink.serializers.short_hash")
    def test_short_link_contains_proper_hash(self, mock_short_hash):
        mock_short_hash.return_value = 12345678
        response = self.client.post(
            "/linkmap/", {"orig_url": "https://foobarbaz.com"}, format="json"
        )
        self.assertEndsWith(response.data["short_url"], "12345678")

    def test_create_same_link_doesnt_change_existing(self):
        _existing = LinkMap.objects.create(
            orig_url="https://foobarbaz.com", url_hash="12341234"
        )
        response = self.client.post(
            "/linkmap/", {"orig_url": "https://foobarbaz.com"}, format="json"
        )
        self.assertTrue(f"{REDIRECT_PATH}12341234" in response.data["short_url"])

    def test_invalid_url_character(self):
        response = self.client.post(
            "/linkmap/", {"orig_url": "https://foobarbaz|com"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_url_protocol(self):
        response = self.client.post(
            "/linkmap/", {"orig_url": "hatetepe://foobarbaz.com"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_url_nonascii(self):
        response = self.client.post(
            "/linkmap/", {"orig_url": "http://foobarbaz.com/ąęęą"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_request_empty_json(self):
        response = self.client.post("/linkmap/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_request_no_required_key(self):
        response = self.client.post("/linkmap/", {"foo": "bar"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reverse_link_map(self):
        _existing = LinkMap.objects.create(
            orig_url="https://foobarbaz.com", url_hash="12341234"
        )
        response = self.client.get("/linkmap/12341234")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"orig_url": "https://foobarbaz.com"})

    def test_reverse_link_map_does_not_exists(self):
        response = self.client.get("/linkmap/12341234")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_redirect(self):
        _existing = LinkMap.objects.create(
            orig_url="https://foobarbaz.com", url_hash="12341234"
        )
        response = self.client.get("/short/12341234")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "https://foobarbaz.com")

    def test_redirect_does_not_exists(self):
        response = self.client.get("/short/12341234")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
