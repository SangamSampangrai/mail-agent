from langchain.tools import tool
from gmail_service import send_email
from pydantic import BaseModel, EmailStr, Field


class EmailRequest(BaseModel):
    to: EmailStr
    subject: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1)


@tool(args_schema=EmailRequest)
def send_email_tool(to: str, subject: str, body: str) -> str:
    """Send a finalized email through Gmail after the user
    explicitly requests sending and confirms the final email."""

    print("\n -- Email Confirmation --")
    print(f"To: {to}")
    print(f"Subject: {subject}")
    print(f"Body: {body}\n")

    confirmation = input("Do you want to send this email? (yes/no): ").strip().lower()

    if confirmation not in ["yes", "y"]:
        return "Email was not sent because user cancelled the operation."

    return send_email(to=to, subject=subject, body=body)
