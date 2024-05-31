from api.views import TextUploadView
from django.urls import path

urlpatterns = [
    path("create-document/", TextUploadView.as_view(), name="create-document"),
]
