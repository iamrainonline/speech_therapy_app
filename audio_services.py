# audio_services.py
"""
Servicii pentru audio (TTS și recunoaștere vocală)
"""
import speech_recognition as sr
import pyttsx3
from abc import ABC, abstractmethod
from typing import Optional
from config import AppConfig

class AudioService(ABC):
    """Interfață abstractă pentru serviciile audio"""
    
    @abstractmethod
    def speak(self, text: str) -> None:
        pass
    
    @abstractmethod
    def listen(self) -> Optional[str]:
        pass

class TTSService:
    """Serviciu pentru text-to-speech"""
    
    def __init__(self, rate: int = AppConfig.SPEECH_RATE):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', rate)
            self._available = True
        except Exception as e:
            print(f"Eroare inițializare TTS: {e}")
            self._available = False
    
    def speak(self, text: str) -> None:
        """Pronunță un text"""
        if not self._available:
            print(f"TTS nu este disponibil. Text: {text}")
            return
            
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Eroare TTS: {e}")
    
    def is_available(self) -> bool:
        """Verifică dacă TTS este disponibil"""
        return self._available

class SpeechRecognitionService:
    """Serviciu pentru recunoașterea vocii"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        try:
            self.microphone = sr.Microphone()
            self._setup_microphone()
            self._available = True
        except Exception as e:
            print(f"Eroare inițializare microfon: {e}")
            self._available = False
    
    def _setup_microphone(self) -> None:
        """Configurează microfonul"""
        if not self._available:
            return
            
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        except Exception as e:
            print(f"Eroare configurare microfon: {e}")
            self._available = False
    
    def listen(self) -> Optional[str]:
        """Ascultă și recunoaște vorbirea"""
        if not self._available:
            return None
            
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source, 
                    timeout=AppConfig.LISTEN_TIMEOUT, 
                    phrase_time_limit=AppConfig.PHRASE_TIME_LIMIT
                )
            
            text = self.recognizer.recognize_google(audio, language='ro-RO')
            return text.lower().strip()
            
        except sr.WaitTimeoutError:
            return "TIMEOUT"
        except sr.UnknownValueError:
            return "UNKNOWN"
        except sr.RequestError as e:
            print(f"Eroare serviciu recunoaștere: {e}")
            return "ERROR"
        except Exception as e:
            print(f"Eroare neașteptată recunoaștere: {e}")
            return "ERROR"
    
    def is_available(self) -> bool:
        """Verifică dacă recunoașterea vocală este disponibilă"""
        return self._available

class CombinedAudioService(AudioService):
    """Serviciu audio combinat (TTS + Recunoaștere)"""
    
    def __init__(self):
        self.tts = TTSService()
        self.stt = SpeechRecognitionService()
    
    def speak(self, text: str) -> None:
        """Pronunță un text"""
        self.tts.speak(text)
    
    def listen(self) -> Optional[str]:
        """Ascultă și recunoaște vorbirea"""
        return self.stt.listen()
    
    def is_tts_available(self) -> bool:
        """Verifică disponibilitatea TTS"""
        return self.tts.is_available()
    
    def is_stt_available(self) -> bool:
        """Verifică disponibilitatea recunoașterii vocale"""
        return self.stt.is_available()
    
    def get_status(self) -> dict:
        """Returnează statusul serviciilor audio"""
        return {
            'tts_available': self.is_tts_available(),
            'stt_available': self.is_stt_available()
        }