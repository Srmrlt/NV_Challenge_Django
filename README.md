# Google Drive File Creator API

This project provides an API method to create a Google Drive document with a specified name and content. The project is implemented using Python, Django, and Django REST Framework (DRF) and is deployed using Docker Compose.

## Prerequisites

Before running this project, you need to set up a Google account and authorize the application to access Google Drive. Follow these steps:

1. Create a Google account if you don't already have one.
2. Go to the Google Cloud Console (https://console.cloud.google.com/).
3. Create a new project.
4. Enable the Google Drive API for your project.
5. Create OAuth 2.0 credentials for your project.
6. Download the credentials JSON file and save it in the `google_secrets` directory as `credentials.json`.
7. Run the application once to generate the token file and complete the OAuth 2.0 flow.

## Project Setup

### Technologies Used

- Python
- Django
- Django REST Framework (DRF)
- Docker
- Docker Compose

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Srmrlt/NV_Challenge_Django.git
    cd NV_Challenge_Django
    ```

2. Place the `credentials.json` file in the `google_secrets` directory.

3. Copy the example environment file and adjust the settings as needed:
    ```sh
    cp .env.example .env
    ```

4. Build and run the application using Docker Compose:
    ```sh
    docker-compose up --build -d
    ```

### API Endpoint

#### Create a Google Drive Document

- **URL:** `/api/create-document/`
- **Method:** `POST`
- **Parameters:**
  - `data`: The content of the file (string).
  - `name`: The name of the file (string).
- **Response:** JSON object with the status of the request.

#### Example Request

```bash
curl -Method Post -Uri http://localhost:80/api/create-document/ `
    -ContentType "application/json" `
    -Body '{
        "data": "This is the content of the file.",
        "name": "my-file.txt"
    }'
```

## Thanks for Visiting!
