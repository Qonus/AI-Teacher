from audio_recording.audio_recording import select_input_device, record_audio
from speech_to_text.stt import initialize_whisper_model, speech_to_text
from chat_bot.gpt import get_gpt_response, create_client
from text_to_speech.tts import text_to_speech
from text_to_image.tti_generation import generate_image_sd
from server import initialize_server, start_server, send_message
import os
import tiktoken
import re

PERSONALITY_FILE = r"teacher_personalities/Kakashi.txt"
GPT_MODEL = "gpt-4"

encoding = tiktoken.encoding_for_model(GPT_MODEL)

def main():
    # initialize server, start listening for clients
    server = initialize_server("127.0.0.1", 6666)
    start_server(server, handle_client)

def handle_client(server, client, address):
    loop()

def loop():
    # Let user choose their input device
    device_index = select_input_device()

    # Get presonality and shove it to gpt via system message
    with open(PERSONALITY_FILE, encoding="utf-8") as file:
        personality = file.read()

    conversation_history = [
        {
            "role": "system",
            "content": personality
        }
    ]

    # Initialize tts
    voice = "en-US-BrianNeural"
    rate = "+0%"

    # Initialize stt
    whisper_model = initialize_whisper_model()
    print("faster whisper model successfully initialized!")

    # Initialize gpt
    print("Start a conversation with GPT-4:")
    gpt_client = create_client()

    while True:
        # Get user's recorded audio
        audio_filepath = "audio_recording/audio_tmp.wav"
        record_audio(device_index, audio_filepath, "space")

        # turn audio into text using speech recognition
        user_input = speech_to_text(audio_filepath, whisper_model)
        os.remove(audio_filepath)

        # Append user input to conversation history
        conversation_history.append({"role": "user", "content": user_input})

        # Get GPT response
        gpt_response = get_gpt_response(conversation_history, gpt_client, GPT_MODEL)
        response = gpt_response
        # Append GPT response to conversation history
        conversation_history.append({"role": "assistant", "content": response})
        print(gpt_response)

        # divide response into commands and textfor tts
        if "~" in gpt_response:
            instructions, response = gpt_response.split("~")
            if " " in instructions:
                voice, rate = instructions.split(" ")
        
        parts = re.split(r'(\[.*?\])', response)

        response = []
        for part in parts:
            if part.startswith('[') and part.endswith(']'):
                response.append({'command': True, 'text': part[1:-1]})
            else:
                response.append({'command': False, 'text': part})

        def handle_command(command):
            if command[0] == "/":
                # send_message(client, command)
                print(f"sent: {command}")
            else:
                generate_image_sd(command)
                print(f"{command} image generated!")
        
        def handle_text(text):
            print(f"GPT-4: [voice: {voice}, rate: {rate}]\n{text}")
            try:
                text_to_speech(text, voice, rate, play=True, remove=True)
            except Exception as error:
                print("An exception occurred:", error)
        
        # Run the response
        for obj in response:
            if obj['command']:
                handle_command(obj['text'])
            else:
                handle_text(obj['text'])

if __name__ == "__main__" :
    # main()
    loop()