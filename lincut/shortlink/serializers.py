from rest_framework import serializers
from shortlink.models import LinkMap
import hashlib
import base64

SERVER_BASENAME = "http://localhost:8000"


class LinkMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkMap
        fields = "__all__"
        read_only_fields = ["url_hash"]

    def create(self, validated_data):
        url_hash = short_hash(validated_data["orig_url"])
        validated_data["url_hash"] = url_hash
        return LinkMap.objects.create(**validated_data)


def short_hash(text):
    digest = hashlib.sha256(text.encode()).digest()
    return base64.urlsafe_b64encode(digest).decode()[:8]
