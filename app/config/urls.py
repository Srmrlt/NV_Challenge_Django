from django.contrib import admin
from django.urls import path

from api.views import TextUploadView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("upload/", TextUploadView.as_view(), name="text-upload"),
]
