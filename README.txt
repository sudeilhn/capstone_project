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





