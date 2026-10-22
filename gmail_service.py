import base64
from email.message import EmailMessage
from googleapiclient.errors import HttpError

from gmail_client import get_gmail_service


def send_email(to: str, subject: str, body: str) -> str:
    """Send an email through email API."""
    service = get_gmail_service()

    # create the email
    message = EmailMessage()
    message["To"] = to
    message["subject"] = subject
    message.set_content(body)

    # Convert email to bytes and encode it
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try:
        # send through api
        result = (
            service.users()
            .messages()
            .send(userId="me", body={"raw": encoded_message})
            .execute()
        )

        return f"email sent successfully. Message ID: {result['id']}"

    except HttpError as error:
        return f"failed to sent email: {error}"
