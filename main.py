from audio_recording.audio_recording import select_input_device, record_audio
from STT.stt import speech_to_text
from chat_bot.gpt import get_gpt_response, create_client
from TTS.tts import text_to_speech
import os

PERSONALITY_FILE = r"AITeacher/teacher_personalities/Kakashi.txt"

def main():
    device_index = select_input_device()

    with open(PERSONALITY_FILE, 'r') as file:
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
        audio_filepath = "AITeacher/audio_recording/audio_tmp.wav"
        record_audio(device_index, audio_filepath)
        user_input = speech_to_text(audio_filepath)
        os.remove(audio_filepath)

        # user_input = input("You: ")

        # if user_input.lower() == "exit":
        #     print("Ending conversation.")
        #     break

        # Append user input to conversation history
        conversation_history.append({"role": "user", "content": user_input})

        # Get GPT response
        gpt_response = get_gpt_response(conversation_history, client=client)
        response = gpt_response
        print(gpt_response)
        if "~" in gpt_response:
            instructions, response = gpt_response.split("~")
            if " " in instructions:
                voice, rate = instructions.split(" ")
        # Append GPT response to conversation history
        conversation_history.append({"role": "assistant", "content": response})

        print(f"GPT-4: [voice: {voice}, rate: {rate}]\n{response}")
        try:
            text_to_speech(response, voice, rate, remove=True)
        except Exception as error:
            print("An exception occurred:", error)

if __name__ == "__main__" :
    main()