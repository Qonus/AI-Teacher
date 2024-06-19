import edge_tts
import asyncio
import pygame
from pygame import mixer
import os
import random

async def text_to_speech_file(text, output_file, voice="en-US-BrianNeural", rate="+0%"):
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_file)

def play_sound(file):
    mixer.init()
    mixer.music.load(file)
    mixer.music.play()

    while mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    mixer.music.stop()
    mixer.quit()
    pygame.quit()

def text_to_speech(text, voice="kk-KZ-DauletNeural", rate="+0%", output_file = "test_tts.mp3", remove = False):
    asyncio.run(text_to_speech_file(text, output_file, voice, rate))
    play_sound(output_file)
    if remove:
        os.remove(output_file)

def main_inf():
    i = 0
    while True:
        i += random.randint(0, 100000)
        text = f"Hey there, sorry I am late! I said it {i} times"
        text_to_speech(text)

def main_test():
    text = f"Hey there, sorry I am late! My name is Kakashi Hatake, but you can call me Kakashi sensei or Kakashi Hokage, I hope we will get along soon"
    text_to_speech(text)

if(__name__ == "__main__"):
    # main_inf()
    main_test()
