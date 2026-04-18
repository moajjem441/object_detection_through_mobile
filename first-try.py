
import cv2
from ultralytics import YOLO

# give your mobile ip and port here
ip = "192.168.0.106"
port = "4747"
url = f"http://{ip}:{port}/mjpegfeed" 


cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("কানেক্ট করা যাচ্ছে না। দয়া করে ফোনের অ্যাপটি রিস্টার্ট করুন এবং অন্য কোনো উইন্ডো বন্ধ করুন।")
else:
    print("সফলভাবে কানেক্ট হয়েছে!")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # এখানে আপনার YOLO প্রসেসিং করতে পারেন
    cv2.imshow("DroidCam 6.5.1 Stream", frame)
    
    if cv2.waitKey(1) & 0xFF == 27: # Esc টিপলে বন্ধ হবে
        break

cap.release()
cv2.destroyAllWindows()