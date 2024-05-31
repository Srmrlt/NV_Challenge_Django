from rest_framework import serializers


class TextUploadSerializer(serializers.Serializer):
    """
    Serializer for handling text file upload data.

    This serializer validates the input data for uploading a text file,
    ensuring that both 'data' and 'name' fields are present and contain
    valid string values.
    """
    data = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
