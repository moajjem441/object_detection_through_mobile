#its for my third eye project to generate the voice accrodign to the esp32 command

from flask import Flask, request
from gtts import gTTS
import os
import pygame
import time


app = Flask(__name__)

# Pygame mixer initialize (একবার করলেই হবে)
pygame.mixer.init()


def play_audio(text):
    try:
        filename = "voice.mp3"
        
        # 1. make audio
        tts = gTTS(text=text, lang='en')
        tts.save(filename)

        # 2.play audio 
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        # 3. wait until the audio finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        # file unload or overright both can be possible
        pygame.mixer.music.unload() 

    except Exception as e:
        print(f"Audio Error: {e}")
        

@app.route('/')
def home():
    return "ESP32 TTS Server is Running!"

@app.route('/tts')
def tts():
    text = request.args.get('text', 'Hello')
    print(f"📢 Received: {text}")
    
    play_audio(text)
    return "OK"


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=False)