import pyaudio
import wave
import keyboard

def list_input_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    devices = []

    for i in range(num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        if device_info.get('maxInputChannels') > 0:
            devices.append((i, device_info.get('name')))
            
    p.terminate()
    return devices

def select_input_device():
    devices = list_input_devices()
    print("Available input devices:")
    for i, device in devices:
        print(f"{i}: {device}")

    device_index = int(input("Select input device index: "))
    return device_index

def record_audio(device_index = 0, output_filename="audio_tmp.wav", record_key='r'):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True, input_device_index=device_index,
                        frames_per_buffer=CHUNK)

    print(f"Press '{record_key}' to start recording and release to stop...")

    frames = []

    try:
        while True:
            if keyboard.is_pressed(record_key):
                data = stream.read(CHUNK)
                frames.append(data)
                print("Recording...", end="\r")
            else:
                if frames:
                    break
    except KeyboardInterrupt:
        pass

    print("\nRecording stopped.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

if __name__ == "__main__":
    device_index = select_input_device()
    record_audio(device_index)
