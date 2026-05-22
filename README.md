# Smart Security System

YOLOv8 tabanlı gerçek zamanlı nesne tespit sistemi.

## Technologies
- YOLOv8
- OpenCV
- Raspberry Pi 4
- Python

## Files
- realtime_detection.py
- merge_and_remap.py
- merge_extra py
- negative_add.py


Bu klasör proje sürecinde kullanılan temel Python kodlarını içermektedir.

-----------------------------------
DOSYALAR(KODLAR) VE GÖREVLERİ
-----------------------------------

merge_and_remap.py

Bu kod, farklı kaynaklardan elde edilen YOLO formatındaki veri setlerini tek bir ortak veri yapısında birleştirmek amacıyla geliştirilmiştir. Kod içerisinde person, knife ve gun sınıfları için ayrı veri setleri tanımlanmış ve tüm veri setleri final_dataset klasörü altında ortak bir eğitim yapısına dönüştürülmüştür.

Kod içerisinde bulunan clear_final_dataset() fonksiyonu mevcut final veri setini temizleyerek yeniden oluşturulmasını sağlamaktadır. copy_single_class_dataset() fonksiyonu ise tek sınıflı veri setlerini kopyalayarak class ID değerlerini proje yapısına uygun şekilde yeniden düzenlemektedir.

People with arms veri seti için geliştirilen copy_people_with_arms() fonksiyonu, birden fazla sınıf içeren etiketleri yeniden eşleştirerek person ve gun sınıflarına dönüştürmektedir. Ayrıca copy_negative_dataset() fonksiyonu ile telefon, kalem ve benzeri negatif veri setleri boş label yapısıyla sisteme eklenmektedir. Bu yapı sayesinde modelin yanlış pozitif üretme oranının azaltılması hedeflenmiştir.

merge_extra.py

Bu kod, mevcut final_dataset veri yapısına ek veri setleri dahil etmek amacıyla geliştirilmiştir. Özellikle person, knife ve gun sınıfları için sonradan eklenen veri setlerinin sisteme kontrollü şekilde eklenmesini sağlamaktadır.

Kod içerisinde HEAD_EXTRA_DATASET, KNIFE_EXTRA_DATASET ve GUN_EXTRA_DATASET değişkenleri ile ek veri setleri tanımlanmıştır. Bu veri setleri proje içerisindeki mevcut eğitim veri yapısına dahil edilmektedir.

convert_label() fonksiyonu, YOLO label dosyaları içerisindeki class ID değerlerini proje sınıf yapısına uygun şekilde yeniden düzenlemektedir. Bu sayede farklı veri setlerinden gelen etiket uyumsuzlukları giderilmektedir.

merge_dataset() fonksiyonu ise görüntü ve label dosyalarını ilgili train, validation ve test klasörlerine kopyalamaktadır. Kopyalama sırasında dosya isimleri yeniden düzenlenmekte ve veri karışıklığının önüne geçilmektedir. Ayrıca her label dosyası otomatik olarak yeni class ID değerlerine dönüştürülmektedir.

Kod sonunda person, knife ve gun sınıfları için ek veri setleri final_dataset yapısına eklenmekte ve model eğitimi için veri çeşitliliği artırılmaktadır. Bu yapı sayesinde modelin farklı görüntü koşullarında daha kararlı sonuçlar üretmesi hedeflenmiştir.

negative_add.py

Bu kod, modelin yanlış pozitif (false positive) üretme oranını azaltmak amacıyla negatif veri setlerini final_dataset içerisine eklemek için geliştirilmiştir. Telefon, kalem ve günlük nesneler içeren görüntüler sisteme boş label dosyaları ile eklenmiş ve modelin bu nesneleri knife veya gun olarak algılamasının azaltılması hedeflenmiştir. Kod ayrıca train, val ve test klasör yapılarını otomatik olarak düzenlemekte ve YOLO veri seti yapısına uygun şekilde dosya kopyalama işlemlerini gerçekleştirmektedir.

realtime_detection.py

Bu kod, YOLOv8 tabanlı gerçek zamanlı nesne tespit sistemi için geliştirilmiştir. Sistem webcam üzerinden canlı görüntü almakta ve eğitilmiş YOLO modeli ile person, knife ve gun sınıflarını gerçek zamanlı olarak tespit etmektedir. Kod içerisinde confidence threshold, minimum alan filtreleme ve gun shape filtering gibi yöntemler kullanılarak yanlış pozitif oranı azaltılmaya çalışılmıştır.

Ayrıca frame stabilization yöntemi ile aynı nesnenin ardışık karelerde doğrulanması sağlanmış ve daha kararlı tespit sonuçları elde edilmiştir. Knife veya gun tespiti belirlenen eşik değerlerini geçtiğinde alarm sistemi devreye girmekte ve kullanıcı uyarılmaktadır. Sistem üzerinde OpenCV kullanılarak bounding box çizimleri, confidence değerleri ve gerçek zamanlı görüntü işlemleri gerçekleştirilmiştir.



# Smart Security System

YOLOv8-based real-time object detection system.

## Technologies
- YOLOv8
- OpenCV
- Raspberry Pi 4
- Python

## Files
- realtime_detection.py
- merge_and_remap.py
- merge_extra.py
- negative_add.py

This folder contains the main Python scripts used during the project development process.

-----------------------------------
FILES (SCRIPTS) AND THEIR PURPOSES
-----------------------------------

merge_and_remap.py

This script was developed to merge multiple YOLO-format datasets obtained from different sources into a single unified dataset structure. Separate datasets for person, knife, and gun classes were defined and combined under the final_dataset directory to create a common training dataset.

The clear_final_dataset() function removes the previous final dataset structure and recreates the required folders. The copy_single_class_dataset() function copies single-class datasets and remaps their class IDs according to the project structure.

The copy_people_with_arms() function was developed specifically for the “People with arms” dataset and remaps multiple class labels into person and gun classes. In addition, the copy_negative_dataset() function adds negative datasets such as phones, pens, and daily objects with empty label files. This structure helps reduce false positive detections during model training.

merge_extra.py

This script was developed to add additional datasets into the existing final_dataset structure. It allows extra datasets related to person, knife, and gun classes to be integrated into the current training dataset in a controlled way.

The HEAD_EXTRA_DATASET, KNIFE_EXTRA_DATASET, and GUN_EXTRA_DATASET variables define the additional datasets used in the project.

The convert_label() function remaps YOLO label class IDs into the project’s class structure. This prevents label inconsistencies between different datasets.

The merge_dataset() function copies image and label files into the train, validation, and test directories. During this process, file names are reorganized to avoid conflicts and labels are automatically converted into the new class ID structure.

At the end of the script, additional person, knife, and gun datasets are merged into the final_dataset structure in order to increase dataset diversity and improve model robustness under different image conditions.

negative_add.py

This script was developed to reduce false positive detections by adding negative datasets into the final_dataset structure. Images containing phones, pens, and other daily objects are added with empty label files so the model learns that these objects are not knife or gun classes.

The script also automatically organizes train, val, and test folder structures and performs dataset copying operations compatible with the YOLO dataset format.

realtime_detection.py

This script was developed for the YOLOv8-based real-time object detection system. The system captures live webcam images and performs real-time detection of person, knife, and gun classes using the trained YOLO model.

The code includes several filtering mechanisms such as confidence thresholding, minimum area filtering, and gun shape filtering in order to reduce false positive detections.

In addition, a frame stabilization mechanism is used to verify detections across multiple consecutive frames, resulting in more stable and reliable outputs. When knife or gun detections exceed predefined thresholds, the alarm system is triggered to warn the user.

OpenCV is used for bounding box visualization, confidence score display, and real-time image processing operations.

weights/

This folder contains the trained YOLOv8 model weight files obtained during the training process. The best-performing model was saved as “best.pt” and used in the real-time object detection system.

The “last.pt” file represents the final state of the training process after the last epoch. The “best.pt” model was mainly used during Raspberry Pi and real-time webcam tests.


