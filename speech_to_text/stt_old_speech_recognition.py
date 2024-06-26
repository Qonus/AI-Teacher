import pyaudio
import speech_recognition as sr
import threading
import keyboard  # For detecting key press

def recognize_speech_from_mic(recognizer, microphone, language='en-US'):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio, language=language)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["success"] = False
        response["error"] = "Unable to recognize speech"

    return response

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Press and hold 'space' to speak...")

    while True:
        if keyboard.is_pressed('space'):
            print("Key pressed. Starting recognition...")
            response = recognize_speech_from_mic(recognizer, microphone  , language='en-US')

            if response["success"]:
                transcription = response["transcription"]
                print("Transcription: ", transcription)
            else:
                print("Error: ", response["error"])
            
            # Wait for the key to be released
            while keyboard.is_pressed('space'):
                pass
            print("Key released. Ready to listen again...")

if __name__ == "__main__":
    main()