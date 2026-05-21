# =========================================================
# DATASET MERGE AND REMAP SCRIPT
# VERİ SETİ BİRLEŞTİRME VE CLASS ID DÖNÜŞTÜRME KODU
# =========================================================

# Import required libraries
# Gerekli kütüphanelerin eklenmesi
from pathlib import Path
import shutil

# =========================
# ANA KLASÖRLER
# MAIN DATASET FOLDERS
# =========================

# Main combined dataset folder
# Birleştirilmiş ana veri seti klasörü
BASE = Path("combined_dataset")

# Final YOLO dataset folder
# Final YOLO veri seti klasörü
FINAL = Path("final_dataset")

# Image and label folders
# Görüntü ve label klasörleri
IMG_DIR = FINAL / "images"
LBL_DIR = FINAL / "labels"

# Supported image formats
# Desteklenen görüntü formatları
IMG_EXTS = {".jpg", ".jpeg", ".png"}

# Create train / val / test folders
# Train / val / test klasörlerini oluştur
for split in ["train", "val", "test"]:
    (IMG_DIR / split).mkdir(parents=True, exist_ok=True)
    (LBL_DIR / split).mkdir(parents=True, exist_ok=True)

# =========================
# DATASETLER
# DATASET DEFINITIONS
# =========================

# Person datasets
# Person veri setleri
PERSON_DATASETS = [
    BASE / "Person Detection.v1i.yolov8",
    BASE / "Head Detection V.5.v3i.yolov8",
]

# Knife datasets
# Knife veri setleri
KNIFE_DATASETS = [
    BASE / "Knife.v2i.yolov8",
    BASE / "Knife.v3i.yolov8",
]

# Gun datasets
# Gun veri setleri
GUN_DATASETS = [
    BASE / "gun.v3i.yolov8",
]

# Mixed dataset containing person and gun classes
# Person ve gun sınıflarını içeren karma veri seti
PEOPLE_WITH_ARMS = BASE / "People with arms.v1i.yolov8"

# Negative datasets for false positive reduction
# False positive azaltmak için kullanılan negatif veri setleri
NEGATIVE_DATASETS = [
    BASE / "phone.v1i.yolov8",
    BASE / "tools.v3i.yolov8",
    BASE / "everyday object detection.v1i.yolov8",
    BASE / "Everyday Stationery Items.v1-roboflow-instant-1--eval-.yolov8",
]

# Roboflow split mapping
# Roboflow veri seti klasör eşleştirmesi
SPLIT_MAP = {
    "train": "train",
    "valid": "val",
    "val": "val",
    "test": "test"
}

# =========================
# TEMİZLEME
# CLEAR FINAL DATASET
# =========================

# Clear old final dataset structure
# Eski final dataset yapısını temizle
def clear_final_dataset():

    if FINAL.exists():
        shutil.rmtree(FINAL, ignore_errors=True)

    # Recreate dataset folders
    # Veri seti klasörlerini yeniden oluştur
    for split in ["train", "val", "test"]:
        (IMG_DIR / split).mkdir(parents=True, exist_ok=True)
        (LBL_DIR / split).mkdir(parents=True, exist_ok=True)

# =========================
# TEK CLASS DATASET KOPYALAMA
# SINGLE CLASS DATASET MERGE
# =========================

# Final project class IDs
# Final proje class ID değerleri

# 0 = person
# 1 = knife
# 2 = gun

# Copy single-class datasets and remap labels
# Tek sınıflı veri setlerini kopyala ve label dönüştür
def copy_single_class_dataset(dataset_path: Path, class_id: int, prefix: str):

    print(f"[+] {dataset_path.name} -> class {class_id}")

    for src_split, dst_split in SPLIT_MAP.items():

        # Source image and label folders
        # Kaynak görüntü ve label klasörleri
        src_img_dir = dataset_path / src_split / "images"
        src_lbl_dir = dataset_path / src_split / "labels"

        if not src_img_dir.exists():
            continue

        copied_count = 0

        # Copy image files
        # Görüntü dosyalarını kopyala
        for img in src_img_dir.iterdir():

            if img.suffix.lower() not in IMG_EXTS:
                continue

            # Create unique file names
            # Benzersiz dosya adı oluştur
            new_name = f"{prefix}_{img.stem}{img.suffix}"

            shutil.copy(img, IMG_DIR / dst_split / new_name)

            # Source and destination label files
            # Kaynak ve hedef label dosyaları
            src_lbl = src_lbl_dir / f"{img.stem}.txt"
            dst_lbl = LBL_DIR / dst_split / f"{prefix}_{img.stem}.txt"

            lines_out = []

            # Convert class IDs
            # Class ID değerlerini dönüştür
            if src_lbl.exists():

                for line in src_lbl.read_text(encoding="utf-8").splitlines():

                    parts = line.split()

                    if len(parts) >= 5:
                        parts[0] = str(class_id)
                        lines_out.append(" ".join(parts))

            # Save converted labels
            # Dönüştürülmüş label dosyasını kaydet
            dst_lbl.write_text("\n".join(lines_out), encoding="utf-8")

            copied_count += 1

        print(f"  - {src_split} -> {dst_split}: {copied_count} görüntü kopyalandı")

# =========================
# PEOPLE WITH ARMS (ÇOKLU CLASS)
# MULTI-CLASS DATASET REMAPPING
# =========================

# Dataset class mappings:
# Veri seti class dönüşümleri:

# Gun   -> gun    -> 2
# Human -> person -> 0
# gun   -> gun    -> 2
# guns  -> gun    -> 2
# person-> person -> 0

# Convert multi-class dataset into project classes
# Çoklu class veri setini proje sınıflarına dönüştür
def copy_people_with_arms(dataset_path: Path):

    print(f"[+] {dataset_path.name} -> mixed class mapping")

    class_map = {
        "0": "2",
        "1": "0",
        "2": "2",
        "3": "2",
        "4": "0",
    }

    for src_split, dst_split in SPLIT_MAP.items():

        # Source image and label folders
        # Kaynak görüntü ve label klasörleri
        src_img_dir = dataset_path / src_split / "images"
        src_lbl_dir = dataset_path / src_split / "labels"

        if not src_img_dir.exists():
            continue

        copied_count = 0

        # Copy image files
        # Görüntü dosyalarını kopyala
        for img in src_img_dir.iterdir():

            if img.suffix.lower() not in IMG_EXTS:
                continue

            new_name = f"arms_{img.stem}{img.suffix}"

            shutil.copy(img, IMG_DIR / dst_split / new_name)

            src_lbl = src_lbl_dir / f"{img.stem}.txt"
            dst_lbl = LBL_DIR / dst_split / f"arms_{img.stem}.txt"

            lines_out = []

            # Convert labels using class map
            # Label dosyalarını class map ile dönüştür
            if src_lbl.exists():

                for line in src_lbl.read_text(encoding="utf-8").splitlines():

                    parts = line.split()

                    if len(parts) >= 5 and parts[0] in class_map:
                        parts[0] = class_map[parts[0]]
                        lines_out.append(" ".join(parts))

            dst_lbl.write_text("\n".join(lines_out), encoding="utf-8")

            copied_count += 1

        print(f"  - {src_split} -> {dst_split}: {copied_count} görüntü kopyalandı")

# =========================
# NEGATİF DATA
# NEGATIVE DATASET ADDITION
# =========================

# Add negative datasets with empty labels
# Negatif veri setlerini boş label ile ekle
def copy_negative_dataset(dataset_path: Path):

    print(f"[+] Negative: {dataset_path.name}")

    for src_split, dst_split in SPLIT_MAP.items():

        src_img_dir = dataset_path / src_split / "images"

        if not src_img_dir.exists():
            continue

        copied_count = 0

        # Copy negative images
        # Negatif görüntüleri kopyala
        for img in src_img_dir.iterdir():

            if img.suffix.lower() not in IMG_EXTS:
                continue

            new_name = f"neg_{dataset_path.stem}_{img.stem}{img.suffix}"

            shutil.copy(img, IMG_DIR / dst_split / new_name)

            # Create empty labels
            # Boş label dosyası oluştur
            (LBL_DIR / dst_split / f"neg_{dataset_path.stem}_{img.stem}.txt").write_text("", encoding="utf-8")

            copied_count += 1

        print(f"  - {src_split} -> {dst_split}: {copied_count} negatif görüntü kopyalandı")

# =========================
# YAML OLUŞTUR
# CREATE YOLO YAML FILE
# =========================

# Create YOLOv8 data.yaml configuration file
# YOLOv8 için data.yaml dosyası oluştur
def create_yaml():

    yaml = """train: images/train
val: images/val
test: images/test

nc: 3
names: ['person', 'knife', 'gun']
"""

    (FINAL / "data.yaml").write_text(yaml, encoding="utf-8")

    print("[+] data.yaml hazır")

# =========================
# ÖZET
# DATASET SUMMARY
# =========================

# Print dataset statistics
# Veri seti özet bilgilerini yazdır
def summarize():

    print("\n=== Final Dataset Özeti ===")

    for split in ["train", "val", "test"]:

        img_count = len(list((IMG_DIR / split).glob("*")))
        lbl_count = len(list((LBL_DIR / split).glob("*.txt")))

        print(f"{split}: {img_count} image | {lbl_count} label")

# =========================
# MAIN
# MAIN EXECUTION BLOCK
# =========================

def main():

    # Clear old dataset
    # Eski veri setini temizle
    clear_final_dataset()

    # Add person datasets
    # Person veri setlerini ekle
    for ds in PERSON_DATASETS:

        if ds.exists():
            copy_single_class_dataset(ds, 0, "person")

        else:
            print(f"[UYARI] Bulunamadı: {ds}")

    # Add knife datasets
    # Knife veri setlerini ekle
    for ds in KNIFE_DATASETS:

        if ds.exists():
            copy_single_class_dataset(ds, 1, "knife")

        else:
            print(f"[UYARI] Bulunamadı: {ds}")

    # Add gun datasets
    # Gun veri setlerini ekle
    for ds in GUN_DATASETS:

        if ds.exists():
            copy_single_class_dataset(ds, 2, "gun")

        else:
            print(f"[UYARI] Bulunamadı: {ds}")

    # Add mixed dataset
    # Karma veri setini ekle
    if PEOPLE_WITH_ARMS.exists():

        copy_people_with_arms(PEOPLE_WITH_ARMS)

    else:
        print(f"[UYARI] Bulunamadı: {PEOPLE_WITH_ARMS}")

    # Add negative datasets
    # Negatif veri setlerini ekle
    for ds in NEGATIVE_DATASETS:

        if ds.exists():
            copy_negative_dataset(ds)

        else:
            print(f"[UYARI] Bulunamadı: {ds}")

    # Create YAML file
    # YAML dosyasını oluştur
    create_yaml()

    # Print dataset summary
    # Veri seti özetini yazdır
    summarize()

    print("\nDATASET HAZIR")
    print(f"Final klasör: {FINAL.resolve()}")

# Program entry point
# Program başlangıç noktası
if __name__ == "__main__":

    main()