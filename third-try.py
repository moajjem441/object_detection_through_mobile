# voice problem done
import cv2
from ultralytics import YOLO
import pyttsx3
import threading
import time

# 1.yolo model load
model = YOLO("yolov8n.pt")

# ভয়েস স্ট্যাটাস চেক করার জন্য একটি গ্লোবাল ভেরিয়েবল
is_speaking = False

# ২. ভয়েস ফাংশন
def speak_task(text):
    global is_speaking
    is_speaking = True
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 160)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"Voice error: {e}")
    finally:
        is_speaking = False # কথা শেষ হলে আবার রেডি হবে

# ৩. ক্যামেরা সেটআপ
url = "http://192.168.0.106:4747/mjpegfeed"
cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)

last_spoken_time = 0
cooldown = 5 # ঠিক ৫ সেকেন্ড পর পর বলবে

print("সিস্টেম চালু হয়েছে। ৫ সেকেন্ড পর পর ভয়েস অ্যালার্ট আসবে...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))

    # ডিটেকশন
    results = model.predict(frame, conf=0.5, verbose=False)
    annotated_frame = results[0].plot()

    current_time = time.time()

    # অবজেক্ট চেক এবং টাইম কন্ডিশন
    if len(results[0].boxes) > 0:
        label = model.names[int(results[0].boxes.cls[0])]
        
        # শর্ত: ৫ সেকেন্ড পার হয়েছে এবং বর্তমানে কোনো ভয়েস চলছে না
        if (current_time - last_spoken_time > cooldown) and not is_speaking:
            print(f"Time to speak: {label}")
            
            # থ্রেড চালু করা
            thread = threading.Thread(target=speak_task, args=(f"I see a {label}",))
            thread.start()
            
            last_spoken_time = current_time

    # রেজাল্ট দেখানো
    cv2.imshow("Third Eye AI", annotated_frame)

    if cv2.waitKey(1) & 0xFF == 27: # Esc টিপলে বন্ধ হবে
        break

cap.release()
cv2.destroyAllWindows()