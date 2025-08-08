# Aplicație Exerciții Pronunție pentru Afazie

O aplicație desktop în Python pentru exerciții de pronunție, special concepută pentru persoanele cu afazie.

## 📁 Structura Proiectului

```
speech_therapy_app/
├── config.py              # Configurări și constante
├── models.py              # Modele de date
├── word_manager.py        # Manager pentru categorii de cuvinte
├── audio_services.py      # Servicii audio (TTS + STT)
├── pronunciation_checker.py # Verificare pronunție
├── ui_components.py       # Componente interfață
├── game_controller.py     # Logica jocului
├── main_app.py           # Aplicația principală
├── requirements.txt      # Dependințe
└── README.md            # Acest fișier
```

## 🚀 Instalare și Rulare

### 1. Instalare Python

Asigură-te că ai Python 3.7+ instalat pe sistem.

### 2. Instalare dependințe

```bash
pip install -r requirements.txt
```

**Pe Windows, dacă întâmpini probleme cu pyaudio:**

```bash
pip install pipwin
pipwin install pyaudio
```

### 3. Rulare aplicație

```bash
python main_app.py
```

## ✨ Funcționalități

- **📢 Afișare cuvinte mari și clare**
- **🎤 Recunoaștere vocală în română**
- **🔊 Pronunție audio a cuvintelor**
- **🟢 Feedback vizual verde pentru pronunție corectă**
- **🔴 Feedback vizual roșu (blink) pentru pronunție incorectă**
- **📊 Sistem de punctaj**
- **📚 Multiple categorii de cuvinte**

## 📚 Categorii Disponibile

- **Animale**: pisică, câine, cal, etc.
- **Obiecte Casă**: masă, scaun, frigider, etc.
- **Corpul Uman**: cap, mână, ochi, etc.
- **Mâncare**: pâine, lapte, mere, etc.
- **Culori**: roșu, verde, albastru, etc.
- **Familie**: mamă, tată, fiu, etc.
- **Numere**: unu, doi, trei, etc.
- **Verbe Simple**: merg, vin, mănânc, etc.

## 🎮 Cum să folosești aplicația

1. **Selectează o categorie** din dropdown
2. **Aplicația afișează un cuvânt** și îl pronunță automat
3. **Apasă butonul 🎤 "Vorbește"** și pronunță cuvântul
4. **Rezultat**:
   - ✅ **Verde** → pronunție corectă, trece la următorul cuvânt
   - ❌ **Roșu blink** → pronunție incorectă, încearcă din nou

## 🔧 Butoane de Control

- **🔊 Ascultă cuvântul**: Redă audio cu pronunția corectă
- **🎤 Vorbește**: Activează microfonul pentru recunoaștere
- **⏭ Sari peste**: Trece la următorul cuvânt fără punctaj
- **🔄 Restart categorie**: Reîncepe categoria curentă

## 🏗️ Arhitectură

Aplicația folosește o arhitectură modulară cu următoarele componente:

- **`config.py`**: Configurări centralizate
- **`models.py`**: Modele de date (GameState, WordCategory)
- **`word_manager.py`**: Gestionează categoriile de cuvinte
- **`audio_services.py`**: Servicii TTS și recunoaștere vocală
- **`pronunciation_checker.py`**: Algoritm de verificare pronunție
- **`ui_components.py`**: Componente UI reutilizabile
- **`game_controller.py`**: Logica principală a jocului
- **`main_app.py`**: Aplicația principală și integrarea UI

## 🔊 Cerințe Audio

- **Microfon funcțional** pentru recunoașterea vocală
- **Boxe/căști** pentru redarea audio
- **Conexiune internet** pentru serviciul Google Speech Recognition

## 🐛 Troubleshooting

### Eroare: "No module named 'pyaudio'"

```bash
# Windows
pip install pipwin
pipwin install pyaudio

# macOS
brew install portaudio
pip install pyaudio

# Linux (Ubuntu/Debian)
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

### Eroare: "Could not understand audio"

- Verifică dacă microfonul funcționează
- Vorbește mai tare și mai clar
- Verifică conexiunea la internet

### Aplicația nu redă sunet

- Verifică volumul sistemului
- Testează cu alte aplicații audio
- Restartează aplicația

## 🤝 Contribuții

Pentru a adăuga categorii noi sau îmbunătățiri:

1. Modifică `word_manager.py` pentru categorii noi
2. Ajustează `pronunciation_checker.py` pentru algoritmi îmbunătățiți
3. Testează cu utilizatori reali

## 📄 Licență

Acest proiect este open source și destinat folosirii în scopuri terapeutice și educaționale.
