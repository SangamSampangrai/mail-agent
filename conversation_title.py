def generate_conversation_title(model, first_message: str) -> str:
    prompt = f""" 
    Generate a short tile for this conversation.
    
    User's first message:
    {first_message}
    
    Rules:
    1.Maximum 6 words
    2.Be specific and descriptive
    3.Return only the title
    4.Do not use quotation marks
    """

    response = model.invoke(prompt)
    return response.content.strip()
