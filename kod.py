import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random

seviyeye_göre_kelimeler = {
    "kolay": [
        "kedi","köpek","elma","süt","güneş","su","ekmek","araba","ev","kapı",
        "masa","kalem","defter","okul","yol","ağaç","çiçek","balık","kuş","deniz",
        "dağ","taş","top","oyun","anne","baba","abi","abla","bebek","yatak",
        "oda","cam","perde","ışık","sabah","akşam","gece","gün","yaz","kış",
        "bahar","rüzgar","yağmur","kar","bulut","göl","dere","çay","park","bahçe"
    ],
    "orta": [
        "arkadaş","pencere","bilgisayar","telefon","kitaplık","kalemlik","televizyon","mutfak","salon","balkon",
        "yemek","kahvaltı","akşam","öğle","çalışmak","okumak","yazmak","dinlemek","anlamak","öğrenmek",
        "koşmak","yürümek","gezmek","bakmak","görmek","duymak","hissetmek","düşünmek","anlatmak","sormak",
        "cevaplamak","yardım","soru","cevap","hikaye","masal","film","dizi","müzik","şarkı",
        "resim","boya","renk","sarı","mavi","kırmızı","yeşil","siyah","beyaz","gri"
    ],
    "zor": [
        "teknoloji","üniversite","telaffuz","hayal gücü","algoritma","programlama","mühendislik","psikoloji","felsefe","sosyoloji",
        "matematik","geometri","trigonometri","istatistik","optimizasyon","verimlilik","performans","geliştirme","entegrasyon","senkronizasyon",
        "analiz","sentez","yorumlama","değerlendirme","karşılaştırma","olasılık","varsayım","hipotez","deneyim","gözlem",
        "araştırma","keşif","inovasyon","yaratıcılık","motivasyon","disiplin","strateji","planlama","organizasyon","yönetim",
        "iletişim","etkileşim","bağlantı","dönüşüm","adaptasyon","optik","mekanik","dinamik","elektronik","biyoteknoloji"
    ]
}

seviye = input("Zorluk seviyesini seçin (kolay, orta, zor): ")

puan = 0
duration = 5
sample_rate = 44100

translator = Translator()
recognizer = sr.Recognizer()

while True:
    kelime = random.choice(seviyeye_göre_kelimeler[seviye])
    

    dogru_cevap = translator.translate(kelime, dest="en").text.lower()
    
    print(f"\nKelime: {kelime}")
    print("İngilizcesini söyle...")

    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    wav.write("output.wav", sample_rate, recording)

    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="en-US").lower()
        print("Senin söylediğin:", text)

        if text == dogru_cevap:
            puan += 3
            print("✅ Doğru! Puan:", puan)
        else:
            puan -= 1
            print(f"❌ Yanlış! Doğru cevap: {dogru_cevap} | Puan: {puan}")

    except sr.UnknownValueError:
        print("Ses anlaşılamadı")
    except sr.RequestError as e:
        print("API hatası:", e)

    if puan >= 10:
        print("🎉 Tebrikler! 10 puana ulaştın!")
        break
    elif puan <= -3:
        print("😢 Maalesef, -3 puana ulaştın. Tekrar dene!")
        break
