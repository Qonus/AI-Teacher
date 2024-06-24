from audio_recording.audio_recording import select_input_device, record_audio
from STT.stt import speech_to_text
from chat_bot.gpt import get_gpt_response, create_client
from TTS.tts import text_to_speech
from text_to_image.tti import get_image_url_unsplash, save_image
from text_to_image.tti_generation import generate_image_sd
import threading
import time
import os
import tiktoken
import re

PERSONALITY_FILE = r"teacher_personalities/Kakashi.txt"
GPT_MODEL = "gpt-4"

encoding = tiktoken.encoding_for_model(GPT_MODEL)

def main():
    device_index = select_input_device()

    with open(PERSONALITY_FILE, encoding="utf-8") as file:
        personality = file.read()

    conversation_history = [
        {
            "role": "system",
            "content": personality
        }
    ]

    print("Start a conversation with GPT-4:")

    client = create_client()

    voice = "en-US-BrianNeural"
    rate = "+0%"

    while True:
        # Get user input
        audio_filepath = "audio_recording/audio_tmp.wav"
        record_audio(device_index, audio_filepath, "space")
        user_input = speech_to_text(audio_filepath)
        os.remove(audio_filepath)

        # user_input = input("You: ")

        # if user_input.lower() == "exit":
        #     print("Ending conversation.")
        #     break

        # Append user input to conversation history
        conversation_history.append({"role": "user", "content": user_input})

        # Get GPT response
        gpt_response = get_gpt_response(conversation_history, client, GPT_MODEL)
        response = gpt_response
        # Append GPT response to conversation history
        conversation_history.append({"role": "assistant", "content": response})

        # handle commands
        print(gpt_response)
        if "~" in gpt_response:
            instructions, response = gpt_response.split("~")
            if " " in instructions:
                voice, rate = instructions.split(" ")
        
        parts = re.split(r'(\[.*?\])', response)

        # Create the structured result
        response = []
        for part in parts:
            if part.startswith('[') and part.endswith(']'):
                response.append({'command': True, 'text': part[1:-1]})
            else:
                response.append({'command': False, 'text': part})

        def handle_command(command):
            generate_image_sd(command)
            print(f"{command} image generated!")
            # image_url = get_image_url_unsplash(command)
            # save_image(image_url)
        
        def handle_text(text):
            print(f"GPT-4: [voice: {voice}, rate: {rate}]\n{text}")
            try:
                text_to_speech(text, voice, rate, play=True, remove=True)
            except Exception as error:
                print("An exception occurred:", error)
        
        for obj in response:
            if obj['command']:
                handle_command(obj['text'])
            else:
                handle_text(obj['text'])

if __name__ == "__main__" :
    main()