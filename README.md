# Gmail AI Agent

An AI-powered Gmail assistant built with Python, LangChain, LangGraph, OpenRouter, and the Gmail API. This project explores how to build an LLM-powered agent that handles natural-language email requests, generates email drafts, sends emails with user confirmation, and preserves conversation state across sessions.

**Project status:** Work in progress 🚧

> **Development notice:** This is a learning and development project, not a production-ready email automation system. Review all generated email content and recipient details before approving a send.

## Features

### Implemented

- **Natural-language interaction:** Accept email requests through a command-line interface.
- **AI-powered email generation:** Generate email subjects and bodies using an LLM accessed through OpenRouter.
- **Gmail integration:** Send emails using the official Gmail API.
- **OAuth 2.0 authentication:** Authorize Gmail access through Google OAuth.
- **Input validation:** Validate email tool inputs with Pydantic, including recipient email addresses and basic subject and body requirements.
- **Send confirmation:** Request yes/no confirmation before the email-sending function proceeds.
- **Persistent conversation state:** Use LangGraph's SQLite checkpointer to restore conversation state across sessions.
- **Conversation management:** Create conversations, resume existing conversations, and generate conversation titles.

### In progress

- More reliable multi-turn email drafting and revision.
- A structured workflow separating drafting, editing, approval, and sending.
- More reliable collection of missing or ambiguous information.
- Stronger enforcement of explicit approval for the final draft.
- Automated tests, improved error handling, and reliability.

**Current limitation:** Although a send-confirmation prompt is implemented, the agent does not yet reliably enforce a complete draft → edit → approve workflow. Do not treat the LLM alone as a security boundary.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application language |
| LangChain | LLM integration and tool interfaces |
| LangGraph | Agent workflow and state management |
| OpenRouter | Access to supported language models through an API |
| Gmail API | Email sending |
| Google OAuth 2.0 | Gmail authorization |
| SQLite | Conversation metadata and checkpoint persistence |
| Pydantic | Input validation |
| python-dotenv | Environment variable configuration |

## How It Works

At a high level, the application follows this workflow:

1. The user starts the CLI and creates or resumes a conversation.
2. The agent processes the user's natural-language email request.
3. The LLM helps generate an email subject and body.
4. The email-sending tool validates its inputs and presents a confirmation prompt.
5. If the user approves, the application attempts to send the email through Gmail.
6. LangGraph's SQLite checkpointer preserves conversation state for later sessions.

The exact interaction and drafting behavior depend on the current agent implementation.

## Project Structure

```text
mail-agent/
├── agent.py                 # Agent initialization and CLI loop
├── tools.py                 # Email tool and confirmation
├── gmail_client.py          # Gmail OAuth authentication
├── gmail_service.py         # Gmail API integration
├── conversation_manager.py  # Create and select conversations
├── conversation_db.py       # Conversation metadata in SQLite
├── conversation_title.py    # Generate conversation titles
├── .gitignore               # Exclude secrets and local files
└── README.md                # Project documentation
```

Local files such as `.env`, `credentials.json`, `token.json`, and generated SQLite databases are created or used during development and should not be committed to version control.

## Getting Started

### Prerequisites

You will need:

- Python installed on your machine.
- A Google account with Gmail.
- An OpenRouter API key.
- A Google Cloud project with the Gmail API enabled.
- Git to clone the repository.

### 1. Clone the repository

```bash
git clone https://github.com/SangamSampangrai/mail-agent.git
cd mail-agent
```

### 2. Create and activate a virtual environment

**macOS / Linux**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

Install the packages currently used by the project:

```bash
python -m pip install langchain langchain-openai langgraph langgraph-checkpoint-sqlite python-dotenv google-api-python-client google-auth-httplib2 google-auth-oauthlib "pydantic[email]"
```

### 4. Configure OpenRouter

Create a `.env` file in the project root:

```dotenv
Nemotron3_API_KEY=your_openrouter_api_key
```

Replace the placeholder with your own API key. The environment variable name must match the one read by the application in `agent.py`.

The model and OpenRouter base URL are configured in the application code. Ensure the selected model supports the API endpoint used by the project.

### 5. Configure Gmail API access

1. Open the [Google Cloud Console](https://console.cloud.google.com/).
2. Create or select a Google Cloud project.
3. Enable the Gmail API.
4. Configure the OAuth consent screen.
5. If the application is in testing mode, add your Google account as a test user where required.
6. Create an OAuth client ID for a **Desktop app**.
7. Download the client credentials and save them as `credentials.json` in the project root.

The application uses the Gmail sending scope:

```text
https://www.googleapis.com/auth/gmail.send
```

On the first run, Google OAuth authorization is initiated and a local `token.json` may be created. Subsequent runs can reuse the stored token while it remains valid.

OAuth configuration and consent requirements depend on your Google Cloud project settings.

### 6. Run the application

```bash
python agent.py
```

Follow the command-line prompts to create a new conversation or resume an existing one.

## Example Interaction

The following illustrates the intended experience; exact behavior may vary with the current implementation.

```text
You: Help me write an email asking my professor
     for an extension.

Agent: What is your professor's email address,
       and what is the reason for the extension?

You: professor@example.com. I need more time
     to complete my assignment.

Agent: [Generates an email draft]

-- Email Confirmation --

To: professor@example.com
Subject: Request for Assignment Extension
Body: [Generated email body]

Do you want to send this email? (yes/no):
```

Always inspect the recipient, subject, and complete body before confirming.

## Conversation Persistence

The application uses LangGraph's SQLite checkpointer to preserve state between interactions.

Each conversation is associated with a unique `thread_id`. Selecting an existing conversation reuses its thread ID so LangGraph can restore the corresponding checkpointed state.

Conversation metadata, including titles and timestamps, is stored separately in SQLite and associated with the relevant thread ID.

This provides per-conversation persistence. It does not automatically implement shared long-term preferences or memory across all conversations.

## Security Considerations

- Keep API keys in environment variables and never hardcode them in source files.
- Do not commit `.env`, `credentials.json`, `token.json`, database files containing private data, or other secrets.
- Apply the principle of least privilege to Google API scopes.
- Review the email recipient, subject, and body before authorizing a send.
- Treat generated content as untrusted until reviewed.
- Do not rely on an LLM prompt alone to enforce authorization or approval.
- Keep dependencies updated and avoid committing sensitive personal information.

A more robust design should enforce approval through application-controlled workflow state, not merely through instructions to the model.

## Roadmap

- [ ] Separate drafting and editing from the email-sending tool.
- [ ] Implement a controlled draft-and-revision loop.
- [ ] Require explicit approval of the final recipient and message before sending.
- [ ] Improve missing-information and ambiguity handling.
- [ ] Add automated tests for validation, approval, cancellation, and sending failures.
- [ ] Improve logging, exception handling, and retry behavior.
- [ ] Add Gmail search and email-reading functionality.
- [ ] Document dependency versions and improve setup reproducibility.

## Learning Objectives

This project is a practical exploration of:

- Building LLM-powered agents with LangChain.
- Designing workflows using LangGraph.
- Integrating language models with external APIs.
- Implementing tool validation and human confirmation.
- Persisting conversational state with SQLite.
- Designing safer and more reliable AI applications.

## Contributing

This project is under active development. Bug reports, suggestions, and contributions are welcome.

When reporting an issue, include relevant error messages and reproduction steps, but never share API keys, OAuth credentials, access tokens, or private email content.

## License

No license has been selected yet. Until a license is added, do not assume that others have permission to reuse, modify, or distribute this project's code.

If you intend to share the project publicly, consider choosing an appropriate open-source license and adding a `LICENSE` file.
