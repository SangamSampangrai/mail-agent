import os
from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from conversation_manager import choose_conversation
from conversation_db import get_conversation_title, update_conversation_title
from conversation_title import generate_conversation_title

from tools import send_email_tool

load_dotenv()

model = ChatOpenAI(
    model="openrouter/free",
    api_key=os.getenv("Nemotron3_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0.4,
)

# Create a checkpointer to save the state of the agent
with SqliteSaver.from_conn_string("checkpoints.db") as checkpointer:

    agent = create_agent(
        model=model,
        tools=[send_email_tool],
        system_prompt=(
            "You are a helpful email assistant. "
            "When the user requests an email, understand the recipient, "
            "purpose, tone, and relevant details. "
            "Ask clarifying questions before drafting if important information "
            "is missing. Do not invent names, facts, or sender details. "
            "Never include placeholders such as '[Your Name]' in a final email. "
            "Show the completed email and obtain explicit confirmation before sending. "
            "Call send_email_tool only when the email is ready to send. "
            "If the user provides additional details, incorporate them before "
            "requesting confirmation. Never treat additional details as permission to send."
        ),
        checkpointer=checkpointer,
    )

    thread_id = choose_conversation(checkpointer)

    # User selected exit/bye
    if thread_id is None:
        print("Exiting program...")
        exit()

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    while True:
        user_input = input("\nYou : ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("Bye!🥺 Come back soon.")
            break

        if not user_input:
            continue

        try:
            result = agent.invoke(
                {"messages": [{"role": "user", "content": user_input}]},
                config,
            )

            print("\nAgent :")
            print(result["messages"][-1].content)

            # generate a title only if this conversation doesn't have one yet
            if get_conversation_title(thread_id) is None:
                try:
                    title = generate_conversation_title(model, user_input)

                    update_conversation_title(thread_id, title)
                    print(f"\n Conversation title: {title}")
                except Exception as e:
                    print(f"\n Waring: could not generate conversation title: {e}")

        except Exception as e:
            print(f"\nError: {e}")
