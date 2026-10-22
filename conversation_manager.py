import uuid

from conversation_db import create_conversation, list_conversations


def create_thread_id() -> str:
    """
    Generate a unique thread ID for the conversation.
    """
    return str(uuid.uuid4())


def choose_conversation(checkpointer) -> str | None:
    """
    Let the user create a new conversation
    or continue an existing conversation.
    """

    # Get conversations from the database
    conversations = list_conversations()

    print("\n1. New conversation")
    print("2. Continue with existing conversation")

    # --------------------------------------------------
    # Choose new or existing conversation
    # --------------------------------------------------

    while True:
        user_input = input("\nChoose an option 1-2: ").strip().lower()

        # Exit the program
        if user_input in ["exit", "bye"]:
            print("\nGoodbye! 👋")
            return None

        try:
            choice = int(user_input)

            # --------------------------------------------------
            # Create a new conversation
            # --------------------------------------------------
            if choice == 1:
                thread_id = create_thread_id()

                create_conversation(thread_id)

                return thread_id

            # --------------------------------------------------
            # Continue with an existing conversation
            # --------------------------------------------------
            if choice == 2:
                break

            print("\nInvalid option. Please choose 1 or 2.")

        except ValueError:
            print("\nInvalid input. Please enter a valid number.")

    # --------------------------------------------------
    # Existing conversation section
    # --------------------------------------------------

    if not conversations:
        print("\nNo existing conversations found.")
        print("Starting a new conversation.")

        thread_id = create_thread_id()

        # Save the new conversation to the database
        create_conversation(thread_id)

        return thread_id

    print("\nExisting conversations:")

    # --------------------------------------------------
    # Display existing conversations
    # --------------------------------------------------

    for index, conversation in enumerate(conversations, start=1):

        # If list_conversations() returns tuples:
        thread_id = conversation[0]
        title = conversation[1]

        display_title = title or "Untitled conversation"

        print(f"{index}. {display_title}")

    # --------------------------------------------------
    # Select an existing conversation
    # --------------------------------------------------

    while True:

        selection = (
            input("\nSelect a conversation " "(or type 'back' to return to the menu): ")
            .strip()
            .lower()
        )

        # Exit the program
        if selection in ["exit", "bye"]:
            print("\nGoodbye! 👋")
            return None

        # Go back to the main conversation menu
        if selection == "back":
            return choose_conversation(checkpointer)

        try:
            selection = int(selection)

        except ValueError:
            print("\nInvalid input. Please enter a valid number.")
            continue

        # Check whether the selected number is valid
        if 1 <= selection <= len(conversations):

            selected_index = selection - 1

            # Get the selected conversation
            selected_conversation = conversations[selected_index]

            # thread_id is the first column
            thread_id = selected_conversation[0]

            return thread_id

        print(
            f"\nInvalid selection. "
            f"Please choose a number from 1-{len(conversations)}."
        )
