from django.shortcuts import redirect
from rest_framework import status

# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from shortlink.models import LinkMap
from shortlink.serializers import LinkMapSerializer
from rest_framework import generics
from urllib.parse import urljoin

SERVER_BASENAME = "http://localhost:8000/"
REDIRECT_PATH = "short/"
REDIRECT_BASE = urljoin(SERVER_BASENAME, REDIRECT_PATH)


class LinkMapList(generics.ListCreateAPIView):
    queryset = LinkMap.objects.all()
    serializer_class = LinkMapSerializer


class CreateLinkMap(APIView):
    def post(self, request, format=None):
        base = f"{request.scheme}://{request.get_host()}/{REDIRECT_PATH}"
        if type(request) == list:
            return Response(
                {"detail": "Request must not be list"}, status.HTTP_400_BAD_REQUEST
            )
        orig_url = request.data.get("orig_url")
        existing_one = LinkMap.objects.filter(orig_url=orig_url).first()
        if existing_one:
            return Response(
                {
                    "short_url": request.build_absolute_uri(
                        urljoin(base, existing_one.url_hash)
                    )
                }
            )
        serializer = LinkMapSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "short_url": request.build_absolute_uri(
                        urljoin(base, serializer.data["url_hash"])
                    )
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReverseLinkMap(APIView):
    def get(self, _request, url_hash, format=None):
        url_map = LinkMap.objects.filter(url_hash=url_hash).first()
        if not url_map:
            return Response(
                {"detail": "No such hash registered"}, status.HTTP_404_NOT_FOUND
            )
        return Response({"orig_url": url_map.orig_url}, status.HTTP_200_OK)


class RedirectView(APIView):
    def get(self, _request, url_hash):
        url_map = LinkMap.objects.filter(url_hash=url_hash).first()
        if not url_map:
            return Response(
                {"detail": "No such hash registered"}, status.HTTP_404_NOT_FOUND
            )
        return redirect(url_map.orig_url)
