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
        
        # ১. make audio
        tts = gTTS(text=text, lang='en')
        tts.save(filename)

        # ২. অডিও প্লে করা
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        # ৩. অডিও শেষ না হওয়া পর্যন্ত অপেক্ষা (অপশনাল কিন্তু নিরাপদ)
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        # ফাইলটি আনলোড করা যাতে পরে আবার ওভাররাইট করা যায়
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