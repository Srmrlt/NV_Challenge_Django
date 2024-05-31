import io
import logging
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload

from config import settings

logger = logging.getLogger("Google Drive API")


class GoogleDriveClient:
    def __init__(self):
        """
        Initializes the GoogleDriveClient instance, setting up initial configurations.
        """
        self.token_file = settings.GOOGLE_TOKEN_FILE
        self.credentials_file = settings.GOOGLE_CREDENTIALS_FILE
        self.scopes = settings.GOOGLE_SCOPES
        self.creds: Credentials | None = None
        self.service = None
        self.initialize_connection()

    def initialize_connection(self) -> None:
        """
        Initializes the connection to Google Drive using an existing token or creating a new one.
        """
        self.creds = self.get_credentials()
        if self.creds and self.creds.valid:
            self.service = self.create_drive_service()
            logger.info("Successfully connected")
        else:
            logger.error("Connection error")

    def get_credentials(self) -> Credentials | None:
        """
        Retrieves credentials from the token file or creates new ones.

        :return: Google Drive credentials.
        """
        creds = self.load_credentials_from_file()
        if not creds or not creds.valid:
            creds = self.refresh_or_create_token(creds)
        return creds

    def load_credentials_from_file(self) -> Credentials | None:
        """
        Loads credentials from the token file.

        :return: Google Drive credentials if they exist, otherwise None.
        """
        if os.path.exists(self.token_file):
            logger.info(f"Loading credentials from {self.token_file}")
            return Credentials.from_authorized_user_file(self.token_file, self.scopes)
        else:
            logger.warning(f"Token file {self.token_file} does not exist")
            return None

    def refresh_or_create_token(self, creds: Credentials | None) -> Credentials:
        """
        Refreshes or creates a new token for accessing Google Drive.

        :param creds: Current credentials (if any).
        :return: Updated or new Google Drive credentials.
        """
        if creds and creds.expired and creds.refresh_token:
            logger.info("Refreshing expired token")
            creds.refresh(Request())
        else:
            logger.info("Creating new token")
            flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.scopes)
            creds = flow.run_local_server(port=0)

        with open(self.token_file, "w") as token:
            token.write(creds.to_json())

        return creds

    def create_drive_service(self):
        """
        Creates and returns the Google Drive service.

        :return: Google Drive service instance or None if there is an error.
        """
        try:
            return build("drive", "v3", credentials=self.creds)
        except HttpError as error:
            logger.error(f"An error occurred creating the service: {error}")
            return None

    def upload_text_file(self, file_name: str, file_content: str, folder_id: str = None) -> str | None:
        """
        Uploads a text file to Google Drive.

        :param file_name: Name of the file to create.
        :param file_content: Content of the file.
        :param folder_id: ID of the folder to save the file to (optional).
        :return: ID of the created file or None if there is an error.
        """
        if not self.service:
            logger.error("Service not initialized")
            return None
        try:
            file = self.service.files().create(
                body=self.create_file_metadata(file_name, folder_id),
                media_body=self.create_media(file_content),
                fields="id"
            ).execute()
            file_id = file.get("id")
            logger.info(f"File created with ID: {file_id}")
            return file_id
        except HttpError as e:
            logger.error(f"An error occurred: {e}")
            return None

    @staticmethod
    def create_file_metadata(file_name: str, folder_id: str | None) -> dict:
        """
        Creates metadata for the file.

        :param file_name: Name of the file.
        :param folder_id: ID of the folder (optional).
        :return: Dictionary with the file metadata.
        """
        file_metadata = {"name": file_name}
        if folder_id:
            file_metadata["parents"] = [folder_id]
        return file_metadata

    @staticmethod
    def create_media(file_content: str) -> MediaIoBaseUpload:
        """
        Creates a MediaIoBaseUpload object for file upload.

        :param file_content: Content of the file.
        :return: MediaIoBaseUpload object.
        """
        file_stream = io.BytesIO(file_content.encode("utf-8"))
        return MediaIoBaseUpload(file_stream, mimetype="text/plain")
