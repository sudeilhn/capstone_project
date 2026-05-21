# =========================================================
# REAL-TIME OBJECT DETECTION SYSTEM
# GERÇEK ZAMANLI NESNE TESPİT SİSTEMİ
# =========================================================

# Import required libraries
# Gerekli kütüphanelerin eklenmesi
from ultralytics import YOLO
import cv2
import time
import threading

# =========================================================
# LOAD YOLO MODEL
# YOLO MODELİNİ YÜKLE
# =========================================================

# Load trained YOLOv8 model
# Eğitilmiş YOLOv8 modelini yükle
model = YOLO("runs/detect/train4/weights/best.pt")

# =========================
# AYARLAR
# SYSTEM SETTINGS
# =========================

# Confidence thresholds for each class
# Her sınıf için confidence threshold değerleri
CONF_THRESHOLDS = {
    "person": 0.25,
    "knife": 0.40,
    "gun": 0.45
}

# Minimum bounding box area filters
# Minimum bounding box alan filtreleri
MIN_AREA = {
    "person": 500,
    "knife": 450,
    "gun": 900
}

# Required frame count for stable detection
# Kararlı tespit için gerekli frame sayısı
REQUIRED_FRAMES = 3

# Alarm cooldown time
# Alarm bekleme süresi
ALERT_COOLDOWN = 2

# Dangerous object classes
# Tehlikeli nesne sınıfları
danger_classes = ["knife", "gun"]

# Alarm timer and frame buffer
# Alarm zamanlayıcısı ve frame buffer
last_alert_time = 0
frame_buffer = []

# =========================
# ALARM
# ALARM SYSTEM
# =========================

# Play warning alarm
# Uyarı alarmı çal
def play_alarm():

    import winsound

    winsound.Beep(1000, 500)

# =========================
# WEBCAM
# CAMERA INITIALIZATION
# =========================

# Open webcam stream
# Webcam görüntüsünü başlat
cap = cv2.VideoCapture(0)

# Set webcam resolution
# Kamera çözünürlüğünü ayarla
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# =========================================================
# MAIN REAL-TIME DETECTION LOOP
# ANA GERÇEK ZAMANLI TESPİT DÖNGÜSÜ
# =========================================================

while True:

    # Read webcam frame
    # Kameradan görüntü oku
    ret, frame = cap.read()

    if not ret:
        break

    # =========================================================
    # YOLO INFERENCE
    # YOLO NESNE TESPİTİ
    # =========================================================

    # Run YOLO model
    # YOLO modelini çalıştır
    results = model(
        frame,
        imgsz=640,
        conf=0.25,
        verbose=False
    )

    current_detections = []

    # Process detection results
    # Tespit sonuçlarını işle
    for r in results:

        for box in r.boxes:

            # Get class information
            # Sınıf bilgilerini al
            cls_id = int(box.cls[0])

            label = model.names[cls_id]

            conf = float(box.conf[0])

            # =========================
            # CONF FILTER
            # CONFIDENCE FILTERING
            # =========================

            # Filter low confidence detections
            # Düşük confidence değerlerini filtrele
            if conf < CONF_THRESHOLDS.get(label, 0.3):
                continue

            # Bounding box coordinates
            # Bounding box koordinatları
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            w = x2 - x1
            h = y2 - y1

            area = w * h

            # =========================
            # AREA FILTER
            # ALAN FİLTRELEME
            # =========================

            # Filter very small detections
            # Çok küçük nesneleri filtrele
            if area < MIN_AREA.get(label, 500):
                continue

            # =========================
            # GUN SHAPE FILTER
            # SİLAH ŞEKİL FİLTRESİ
            # =========================

            # Additional gun shape filtering
            # Ek silah şekil filtreleme
            if label == "gun":

                ratio = w / h if h != 0 else 0

                if ratio < 1.1:
                    continue

            # Store detections
            # Tespitleri kaydet
            current_detections.append((label, conf))

            # =========================
            # RENKLER
            # BOX COLORS
            # =========================

            # Set box colors for each class
            # Her sınıf için kutu renkleri
            if label == "person":
                color = (0, 255, 0)

            elif label == "knife":
                color = (0, 0, 255)

            elif label == "gun":
                color = (0, 165, 255)

            else:
                color = (255, 255, 255)

            # =========================
            # BOX ÇİZ
            # DRAW BOUNDING BOX
            # =========================

            # Draw detection box
            # Tespit kutusunu çiz
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                color,
                2
            )

            # Draw class label and confidence
            # Sınıf etiketi ve confidence değeri çiz
            cv2.putText(
                frame,
                f"{label} {conf:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )

    # =========================
    # STABLE DETECTION BUFFER
    # FRAME STABILIZATION
    # =========================

    # Add detections into frame buffer
    # Tespitleri frame buffer içerisine ekle
    frame_buffer.append(current_detections)

    # Keep buffer size stable
    # Buffer boyutunu sabit tut
    if len(frame_buffer) > REQUIRED_FRAMES:
        frame_buffer.pop(0)

    danger_detected = False
    danger_label = None

    # Verify detections across multiple frames
    # Nesneleri birden fazla frame üzerinde doğrula
    if len(frame_buffer) == REQUIRED_FRAMES:

        for label in danger_classes:

            if all(
                any(d[0] == label for d in f)
                for f in frame_buffer
            ):
                danger_detected = True
                danger_label = label
                break

    # =========================
    # ALARM SYSTEM
    # ALARM KONTROLÜ
    # =========================

    current_time = time.time()

    # Trigger alarm if danger detected
    # Tehlikeli nesne algılanırsa alarm çalıştır
    if (
        danger_detected and
        current_time - last_alert_time > ALERT_COOLDOWN
    ):

        print(f"🚨 DANGER DETECTED: {danger_label}")

        threading.Thread(
            target=play_alarm,
            daemon=True
        ).start()

        last_alert_time = current_time

    # =========================
    # FPS TEXT
    # EKRAN YAZISI
    # =========================

    # Display system title
    # Sistem başlığını göster
    cv2.putText(
        frame,
        "YOLOv8 Real-Time Detection",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    # Show output window
    # Çıkış ekranını göster
    cv2.imshow("Smart Security System", frame)

    # Exit with Q key
    # Q tuşu ile çıkış yap
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release webcam
# Kamerayı serbest bırak
cap.release()

# Close all windows
# Tüm pencereleri kapat
cv2.destroyAllWindows()

