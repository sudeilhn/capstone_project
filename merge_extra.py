# =========================================================
# EXTRA DATASET MERGE SCRIPT
# EKSTRA VERİ SETİ BİRLEŞTİRME KODU
# =========================================================

# Import required libraries
# Gerekli kütüphanelerin eklenmesi
from pathlib import Path
import shutil

# =========================
# ANA KLASÖRLER
# MAIN DATASET FOLDERS
# =========================

# Combined dataset folder
# Birleştirilmiş veri seti klasörü
BASE_DATASET = Path("combined_dataset")

# Final YOLO dataset folder
# Final YOLO veri seti klasörü
FINAL_DATASET = Path("final_dataset")

# Supported image formats
# Desteklenen görüntü formatları
IMG_EXTS = {".jpg", ".jpeg", ".png"}

# =========================
# EXTRA DATASETLER
# EXTRA DATASET DEFINITIONS
# =========================

# Extra person/head dataset
# Ek person/head veri seti
HEAD_EXTRA_DATASET = BASE_DATASET / "Head Detection V.5.v1i.yolov8" / "Head Detection V.5.v1i.yolov8 kopyası"

# Extra knife dataset
# Ek knife veri seti
KNIFE_EXTRA_DATASET = BASE_DATASET / "Knife Dataset.v1i.yolov8"

# Extra gun dataset
# Ek gun veri seti
GUN_EXTRA_DATASET = BASE_DATASET / "Weapon detection.v1i.yolov8"

# Final project class IDs
# Final proje sınıf etiketleri

# 0 = person
# 1 = knife
# 2 = gun

# Dataset split mapping
# Veri seti klasör eşleştirmesi
SPLIT_MAP = {
    "train": "train",
    "valid": "val",
    "val": "val",
    "test": "test"
}

# =========================
# LABEL DÖNÜŞTÜRME
# LABEL CONVERSION FUNCTION
# =========================

# Convert labels into project class IDs
# Label etiketlerini proje class ID yapısına dönüştürür
def convert_label(file_path: Path, new_class_id: int):

    # Create empty label file if label does not exist
    # Label dosyası yoksa boş txt oluştur
    if not file_path.exists():
        file_path.write_text("", encoding="utf-8")
        return

    # Read label lines
    # Label satırlarını oku
    with file_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []

    # Replace old class IDs with new IDs
    # Eski class ID değerlerini yeni değerlerle değiştir
    for line in lines:
        parts = line.strip().split()

        if len(parts) >= 5:
            parts[0] = str(new_class_id)
            new_lines.append(" ".join(parts) + "\n")

    # Save converted labels
    # Dönüştürülmüş label dosyasını kaydet
    with file_path.open("w", encoding="utf-8") as f:
        f.writelines(new_lines)

# =========================
# DATASET EKLEME
# DATASET MERGE FUNCTION
# =========================

# Merge extra datasets into final_dataset
# Ek veri setlerini final_dataset içerisine ekler
def merge_dataset(source_dataset: Path, class_id: int, prefix: str):

    print(f"\n[+] Dataset ekleniyor: {source_dataset}")

    # Check dataset existence
    # Veri setinin varlığını kontrol et
    if not source_dataset.exists():
        print(f"❌ Dataset bulunamadı: {source_dataset}")
        return

    # Process dataset splits
    # Train / val / test klasörlerini işle
    for src_split, dst_split in SPLIT_MAP.items():

        # Source image and label folders
        # Kaynak görüntü ve label klasörleri
        src_img = source_dataset / src_split / "images"
        src_lbl = source_dataset / src_split / "labels"

        print(f"Checking: {src_img}")

        # Skip missing folders
        # Eksik klasörleri atla
        if not src_img.exists():
            print(f"❌ YOK: {src_img}")
            continue

        print("✔ bulundu")

        # Destination folders
        # Hedef klasörler
        dst_img = FINAL_DATASET / "images" / dst_split
        dst_lbl = FINAL_DATASET / "labels" / dst_split

        # Create destination folders
        # Hedef klasörleri oluştur
        dst_img.mkdir(parents=True, exist_ok=True)
        dst_lbl.mkdir(parents=True, exist_ok=True)

        copied_img_count = 0
        copied_lbl_count = 0

        # Image copy process
        # Görüntü dosyalarını kopyala
        for file in src_img.iterdir():

            # Skip unsupported files
            # Desteklenmeyen dosyaları atla
            if file.suffix.lower() not in IMG_EXTS:
                continue

            # Create unique image names
            # Benzersiz dosya adı oluştur
            new_name = f"{prefix}_{source_dataset.stem}_{file.name}"

            # Copy image file
            # Görüntü dosyasını kopyala
            shutil.copy(file, dst_img / new_name)

            copied_img_count += 1

        # Label copy and conversion process
        # Label kopyalama ve dönüştürme işlemi
        if src_lbl.exists():

            for file in src_lbl.iterdir():

                # Process txt label files only
                # Sadece txt label dosyalarını işle
                if file.suffix.lower() != ".txt":
                    continue

                # Create unique label names
                # Benzersiz label adı oluştur
                new_name = f"{prefix}_{source_dataset.stem}_{file.name}"

                new_path = dst_lbl / new_name

                # Copy label file
                # Label dosyasını kopyala
                shutil.copy(file, new_path)

                # Convert class IDs
                # Class ID değerlerini dönüştür
                convert_label(new_path, class_id)

                copied_lbl_count += 1

        # Print copy summary
        # Kopyalama özetini yazdır
        print(f"  -> {src_split} / {dst_split}: {copied_img_count} image, {copied_lbl_count} label")

# =========================
# MAIN
# MAIN EXECUTION BLOCK
# =========================

if __name__ == "__main__":

    # Add extra person dataset
    # Ek person veri setini ekle
    print("Person extra dataset ekleniyor...")
    merge_dataset(HEAD_EXTRA_DATASET, 0, "person_extra")

    # Add extra knife dataset
    # Ek knife veri setini ekle
    print("\nKnife extra dataset ekleniyor...")
    merge_dataset(KNIFE_EXTRA_DATASET, 1, "knife_extra")

    # Add extra gun dataset
    # Ek gun veri setini ekle
    print("\nGun extra dataset ekleniyor...")
    merge_dataset(GUN_EXTRA_DATASET, 2, "gun_extra")

    # Final process message
    # İşlem tamamlandı mesajı
    print("\n✅ EXTRA DATASET EKLEME TAMAMLANDI")