import os
import asyncio

from dotenv import load_dotenv
from openai import OpenAI
from TTS.tts import text_to_speech

load_dotenv()

GPT_MODEL = "gpt-4"


def create_client():
    return OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),  # Use environment variable for security
    )


def get_gpt_response(conversation_history: list, client):
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=conversation_history,
    )
    response = response.to_dict()
    return response["choices"][0]["message"]["content"]


def main():
    conversation_history = [
        {"role": "system", "content": "You are a Kakashi Sensei."}
    ]

    print("Start a conversation with GPT-4 (type 'exit' to stop):")

    client = create_client()

    while True:
        # Get user input
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Ending conversation.")
            break

        # Append user input to conversation history
        conversation_history.append({"role": "user", "content": user_input})

        # Get GPT response
        gpt_response = get_gpt_response(conversation_history, client=client)

        # Append GPT response to conversation history
        conversation_history.append({"role": "assistant", "content": gpt_response})

        # Print GPT response (optional)
        print(f"GPT-4: {gpt_response}")

        # Call the TTS module to speak the response (assuming tts.py exists)
        text_to_speech(gpt_response) # Call the function from tts.py
    
    return 3

if __name__ == "__main__":
    main()