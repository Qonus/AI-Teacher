from faster_whisper import WhisperModel
import os

def initialize_whisper_model(model = "large-v3"):
    model = WhisperModel(model, device="cuda", compute_type="float16")
    return model

def speech_to_text(audio_filepath, model):
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
    model = initialize_whisper_model()
    speech_to_text(r"audio_recording/audio_tmp.wav", model)