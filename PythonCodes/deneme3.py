import os
import time
from datetime import datetime

def shutdown_at(target_time):
    """
    Belirtilen saate göre Windows sistemini kapatır.
    Açık olan uygulamaları kapatır ve shutdown işlemini başlatır.
    """
    # Kullanıcının girdiği hedef saat (sadece saat)
    target_time = datetime.strptime(target_time, "%H:%M:%S").time()

    print(f"Bilgisayar {target_time} saatinde kapatılacak.")
    
    while True:
        # Şu anki zamanı kontrol et
        current_time = datetime.now().time()

        # Hedef zamana ulaşıldığında işlemi başlat
        if current_time >= target_time:
            print("Tüm açık uygulamalar kapatılıyor...")
            
            # Tüm açık uygulamaları kapat
            #os.system("taskkill /F /FI \"status eq running\"")

            print("Sistem kapatılıyor...")
            
            # Windows sistemini kapat
            os.system("shutdown /f /s /t 0")
            break

        # Bekleme (1 saniye)
        time.sleep(1)

# Kullanıcıdan saat bilgisi al
target_time = input("Kapatma işlemi için saat girin (HH:MM:SS formatında, 24 saatlik dilimde): ")

# Shutdown işlemini başlat
shutdown_at(target_time)