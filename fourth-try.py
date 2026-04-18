# accurate


import cv2
from ultralytics import YOLO
import pyttsx3
import threading
import time

#1.model load(model switch from nano to small to get better accuracy)
model = YOLO("yolov8s.pt") 

#  global variable for checking the voice status
is_speaking = False

# ২. ভয়েস ফাংশন (Backgroud Thread এ চলবে)
def speak_task(text):
    global is_speaking
    is_speaking = True
    try:
        # ইঞ্জিনের নতুন ইনস্ট্যান্স তৈরি
        engine = pyttsx3.init()
        engine.setProperty('rate', 160) # কথা বলার গতি
        engine.setProperty('volume', 1.0) # ভলিউম ফুল
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"ভয়েস এরর: {e}")
    finally:
        is_speaking = False

# ৩. ক্যামেরা এবং ভিডিও সেটআপ
# DroidCam এর আইপি এবং পোর্ট নিশ্চিত করুন
url = "http://192.168.0.106:4747/mjpegfeed"
cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)

# ল্যাগ কমাতে বাফার সাইজ সেট করা
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

last_spoken_time = 0
cooldown_period = 5  # ঠিক ৫ সেকেন্ড পর পর বলবে

print("Third Eye AI সিস্টেম চালু হচ্ছে...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("ক্যামেরা থেকে ফ্রেম পাওয়া যাচ্ছে না!")
        break

    # একুরেসি ঠিক রাখতে ইমেজ সাইজ ৬৪০x৬৪০ এ রিসাইজ করা ভালো
    display_frame = cv2.resize(frame, (640, 480))

    # ৪. YOLO ডিটেকশন (সবচেয়ে ভালো একুরেসির জন্য প্যারামিটার সেট করা)
    results = model.predict(
        source=display_frame, 
        conf=0.45,       # কনফিডেন্স ০.৪৫ (ব্যালেন্সড একুরেসি)
        iou=0.45,        # একই জায়গায় অনেকগুলো বক্স আসা কমাবে
        imgsz=640,       # মডেলের ইন্টারনাল সাইজ
        verbose=False    # টার্মিনালে হিজিবিজি কমাবে
    )

    # রেজাল্ট প্লট করা
    annotated_frame = results[0].plot()

    # ৫. টাইমিং এবং ভয়েস লজিক
    current_time = time.time()
    
    # যদি কোনো অবজেক্ট ডিটেক্ট হয়
    if len(results[0].boxes) > 0:
        # সবচেয়ে বেশি নিশ্চিত (First confidence box) অবজেক্টটি নেওয়া
        cls_id = int(results[0].boxes.cls[0])
        label = model.names[cls_id]

        # ৫ সেকেন্ড গ্যাপ এবং ইঞ্জিন বিজি কি না চেক করা
        if (current_time - last_spoken_time > cooldown_period) and not is_speaking:
            print(f"বলছি: {label}")
            
            # নতুন থ্রেডে ভয়েস চালানো
            speech_thread = threading.Thread(target=speak_task, args=(f"I see a {label}",))
            speech_thread.start()
            
            last_spoken_time = current_time

    # ৬. স্ক্রিনে ভিডিও দেখানো
    cv2.imshow("Third Eye AI - Practice Mode", annotated_frame)

    # Esc কি চাপলে বন্ধ হবে
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()