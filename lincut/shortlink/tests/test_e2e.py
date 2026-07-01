from rest_framework.test import APILiveServerTestCase
import requests
from rest_framework import status
from shortlink.views import SERVER_BASENAME


class ShortLinkE2E(APILiveServerTestCase):
    def test_create_reverse_redirect(self):
        long_link = "https://developers.thecatapi.com/view-account/ylX4blBYT9FaoVd6OhvR?report=bOoHBz-8t"
        client = requests.session()
        response = client.post(
            f"{self.live_server_url}/linkmap/", json={"orig_url": long_link}
        )
        # POST response assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        self.assertEqual(set(body.keys()), {"short_url"})
        short_url = body["short_url"]
        self.assertTrue(short_url.startswith(self.live_server_url))
        # check if link returned really redirects
        redirect_response = client.get(
            short_url,
            allow_redirects=False,
        )
        self.assertEqual(
            redirect_response.status_code,
            status.HTTP_302_FOUND,
        )
        self.assertEqual(
            redirect_response.headers["Location"],
            long_link,
        )
        # check reverse link map
        short_hash = short_url.split("/")[-1]
        reverse_response = client.get(f"{self.live_server_url}/linkmap/{short_hash}")
        body = reverse_response.json()
        self.assertEqual(body, {"orig_url": long_link})
