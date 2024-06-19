from faster_whisper import WhisperModel
import os

def speech_to_text(audio_filepath, model = "large-v3"):
    model = WhisperModel(model, device="cuda", compute_type="float16")

    # or run on GPU with INT8
    # model = WhisperModel(model, device="cuda", compute_type="int8_float16")
    # or run on CPU with INT8
    # model = WhisperModel(model, device="cpu", compute_type="int8")

    file_path = audio_filepath

    if os.path.exists(file_path):
        segments, info = model.transcribe(file_path)

        print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
        
        result = ""
        for segment in segments:
            print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            result += segment.text
        
        return result
    else:
        print(f"Error: File '{file_path}' not found.")

if __name__ == "__main__":
    speech_to_text(r"AITeacher/audio_recording/test_tts.mp3")