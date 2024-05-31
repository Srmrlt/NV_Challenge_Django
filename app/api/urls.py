from django.urls import path

from api.views import TextUploadView

urlpatterns = [
    path("create-document/", TextUploadView.as_view(), name="create-document"),
]
