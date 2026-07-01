from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from shortlink import views

urlpatterns = [
    path("linkmap_all/", views.LinkMapList.as_view()),
    path("linkmap/", views.CreateLinkMap.as_view()),
    path("linkmap/<str:url_hash>", views.ReverseLinkMap.as_view()),
    path(f"{views.REDIRECT_PATH}<str:url_hash>", views.RedirectView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
