import cv2
from ultralytics import YOLO
import pyttsx3
import threading
import time

# ১. YOLO মডেল লোড (প্রথমে ছোট মডেল yolov8n ব্যবহার করা ভালো)
model = YOLO("yolov8n.pt")

# ২. ভয়েস ইঞ্জিন সেটআপ
engine = pyttsx3.init()
def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        pass

# ৩. DroidCam এর IP এবং Port
ip = "192.168.0.106"
port = "4747"
url = f"http://{ip}:{port}/mjpegfeed" 

cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)

last_spoken_time = 0
cooldown = 3 # ৩ সেকেন্ড পরপর কথা বলবে

if not cap.isOpened():
    print("কানেক্ট করা যাচ্ছে না!")
else:
    print("সফলভাবে কানেক্ট হয়েছে এবং অবজেক্ট ডিটেকশন শুরু হচ্ছে...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ইমেজ প্রসেসিং ফাস্ট করার জন্য রিসাইজ
    frame = cv2.resize(frame, (640, 480))

    # ৪. YOLO দিয়ে অবজেক্ট ডিটেক্ট করা
    # stream=True দিলে মেমোরি কম খরচ হয়
    results = model(frame, conf=0.4, verbose=False) 

    # ৫. ফ্রেমের ওপর বক্স এবং লেবেল আঁকা
    annotated_frame = results[0].plot()

    # ৬. ডিটেক্টেড অবজেক্টের নাম বের করা এবং ভয়েস অ্যালার্ট দেওয়া
    if len(results[0].boxes) > 0:
        # প্রথম অবজেক্টের আইডি নেওয়া
        cls_id = int(results[0].boxes.cls[0])
        label = model.names[cls_id]
        
        current_time = time.time()
        if current_time - last_spoken_time > cooldown:
            print(f"Detected: {label}")
            # থ্রেডিং ব্যবহার করা হয়েছে যাতে ভয়েস চলাকালীন ভিডিও আটকে না যায়
            threading.Thread(target=speak, args=(f"I see a {label}",)).start()
            last_spoken_time = current_time

    # রেজাল্ট উইন্ডোতে দেখানো
    cv2.imshow("Third Eye - Object Detection", annotated_frame)
    
    if cv2.waitKey(1) & 0xFF == 27: # Esc টিপলে বন্ধ হবে
        break

cap.release()
cv2.destroyAllWindows()