# =========================================================
# NEGATIVE DATASET ADDITION SCRIPT
# NEGATİF VERİ SETİ EKLEME KODU
# =========================================================

# Import required libraries
# Gerekli kütüphanelerin eklenmesi
import os
import shutil
from pathlib import Path

# =========================
# NEGATIVE DATASETLER
# NEGATIVE DATASET DEFINITIONS
# =========================

# Main dataset folder
# Ana veri seti klasörü
BASE = Path("combined_dataset")

# Negative datasets used for false positive reduction
# False positive azaltmak için kullanılan negatif veri setleri
NEGATIVE_DATASETS = [
    BASE / "indoor objects.v1i.yolov8",
    BASE / "mobile Phone.v1i.yolov8",
    BASE / "pen-detect.v1i.yolov8"
]

# =========================
# HEDEF DATASET
# TARGET FINAL DATASET
# =========================

# Final YOLO dataset folder
# Final YOLO veri seti klasörü
FINAL_DATASET = Path("final_dataset")

# Dataset split folders
# Veri seti split klasörleri
SPLITS = ["train", "valid", "val", "test"]

# Supported image formats
# Desteklenen görüntü formatları
IMG_EXTS = [".jpg", ".jpeg", ".png"]

# =========================
# NEGATIVE DATASET EKLEME
# ADD NEGATIVE DATASETS
# =========================

# Add negative datasets into final_dataset
# Negatif veri setlerini final_dataset içerisine ekler
def add_negatives():

    # Process all negative datasets
    # Tüm negatif veri setlerini işle
    for dataset in NEGATIVE_DATASETS:

        print(f"\n[+] Processing: {dataset}")

        # Process dataset splits
        # Train / val / test klasörlerini işle
        for split in SPLITS:

            # Source image folder
            # Kaynak görüntü klasörü
            src_img = dataset / split / "images"

            # Skip missing folders
            # Eksik klasörleri atla
            if not src_img.exists():
                continue

            # Convert valid -> val for YOLO compatibility
            # YOLO uyumluluğu için valid -> val dönüşümü
            dst_split = "val" if split == "valid" else split

            # Destination image and label folders
            # Hedef görüntü ve label klasörleri
            dst_img = FINAL_DATASET / "images" / dst_split
            dst_lbl = FINAL_DATASET / "labels" / dst_split

            # Create destination folders
            # Hedef klasörleri oluştur
            os.makedirs(dst_img, exist_ok=True)
            os.makedirs(dst_lbl, exist_ok=True)

            # Process image files
            # Görüntü dosyalarını işle
            for img in src_img.iterdir():

                # Skip unsupported formats
                # Desteklenmeyen dosyaları atla
                if img.suffix.lower() not in IMG_EXTS:
                    continue

                # Create unique image names
                # İsim çakışmasını önlemek için benzersiz ad oluştur
                new_name = f"neg_{dataset.stem}_{img.name}"

                # Copy image file
                # Görüntü dosyasını kopyala
                target_img = dst_img / new_name
                shutil.copy(img, target_img)

                # Create empty labels
                # Boş label dosyası oluştur
                label_name = new_name.rsplit(".", 1)[0] + ".txt"

                target_label = dst_lbl / label_name

                # Empty label = no object
                # Boş label = nesne yok
                open(target_label, "w").close()

        print("✔ tamamlandı")

    # Final process message
    # İşlem tamamlandı mesajı
    print("\n TÜM NEGATİF DATASETLER EKLENDİ ")

# =========================
# MAIN
# MAIN EXECUTION BLOCK
# =========================

# Program entry point
# Program başlangıç noktası
if __name__ == "__main__":

    add_negatives()