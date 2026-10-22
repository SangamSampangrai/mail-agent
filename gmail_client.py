import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def get_gmail_service():
    creds = None

    # 1. Try to load previously saved credentials
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # 2. If credentials are missing or invalid
    if not creds or not creds.valid:

        # 3. Try to refresh expired credentials
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        # 4. Otherwise, authenticate through browser
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)

            creds = flow.run_local_server(port=0)

        # 5. Save credentials for future use
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # 6. Create Gmail API client
    service = build("gmail", "v1", credentials=creds)

    return service
