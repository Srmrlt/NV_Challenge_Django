import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import TextUploadSerializer
from api.services import GoogleDriveClient
from config import settings

logger = logging.getLogger(__name__)


class TextUploadView(APIView):
    """
    API view to handle text file uploads to Google Drive.

    This view accepts POST requests with 'data' and 'name' fields.
    It validates the input, uploads the file to Google Drive,
    and returns a response indicating the success or failure of the upload.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the view with a Google Drive client instance.
        """
        super().__init__(*args, **kwargs)
        self.google_drive_service = GoogleDriveClient()

    def post(self, request):
        """
        Handle POST requests to upload a text file to Google Drive.

        Args:
            request (HttpRequest): The request object containing 'data' and 'name' fields.

        Returns:
            Response: A DRF Response object with a success message and file ID if the upload
            is successful, or an error message if it fails.
        """
        serializer = TextUploadSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data['data']
            name = serializer.validated_data['name']

            file_id = self.google_drive_service.upload_text_file(
                file_name=name,
                file_content=data,
                folder_id=settings.GOOGLE_FOLDER_ID
            )
            if file_id:
                return Response(
                    {"message": "File upload success", "file_id": file_id},
                    status=status.HTTP_201_CREATED
                )
            else:
                logger.error("File upload failed: No file ID returned")
                return Response(
                    {"error": "File upload failed"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
