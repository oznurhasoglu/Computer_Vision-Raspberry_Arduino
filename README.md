# Computer Vision With Raspberry and Arduino

Bu proje, bir Raspberry Pi ve kamera modülü aracılığıyla renk tespiti yapar ve Arduino'ya bir çıktı göndererek çıktıya göre LED'in yanıp sönmesini sağlar.

## Gereksinimler

### Yazılım

- Python 3
- OpenCV
- numpy
- RPi.GPIO
- pyserial
- Arduino IDE

### Donanım

- Raspberry Pi
- Arduino
- Kamera modülü
- LED
- Bağlantı kabloları

## Kurulum ve Kullanım

### Arduino

1. Arduino'yu bilgisayara bağlayın.
2. `haberlesme.ino` dosyasını Arduino IDE ile açın.
3. Kodu Arduino'ya yükleyin.

### Raspberry Pi

1. Raspberry Pi'ye gerekli Python kütüphanelerini yükleyin:
    ```bash
    pip install opencv-python numpy RPi.GPIO pyserial
    ```
2. `renk_tespit_rp_arduino.py` dosyasını çalıştırın:
    ```bash
    python3 renk_tespit_rp_arduino.py
    ```
