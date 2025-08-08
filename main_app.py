# main_app.py
"""
Aplicația principală pentru exerciții de pronunție
"""
import tkinter as tk
from tkinter import messagebox
from config import AppConfig, Colors, UIText
from game_controller import GameController
from ui_components import (
    WordDisplayComponent, CategorySelectorComponent, ScoreDisplayComponent,
    StatusDisplayComponent, ControlPanelComponent
)

class SpeechTherapyApp:
    """Aplicația principală pentru terapia vocală"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.controller = GameController()
        self._setup_window()
        self._create_ui()
        self._setup_controller_callbacks()
        self._initialize_game()
    
    def _setup_window(self) -> None:
        """Configurează fereastra principală"""
        self.root.title(AppConfig.WINDOW_TITLE)
        self.root.geometry(AppConfig.WINDOW_SIZE)
        self.root.configure(bg=Colors.BACKGROUND)
        self.root.resizable(True, True)
        
        # Centrare fereastră
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"800x600+{x}+{y}")
    
    def _create_ui(self) -> None:
        """Creează interfața utilizatorului"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg=Colors.BACKGROUND)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Titlu
        title_label = tk.Label(
            main_frame, 
            text=UIText.TITLE, 
            font=('Arial', 24, 'bold'), 
            bg=Colors.BACKGROUND, 
            fg=Colors.TEXT_PRIMARY
        )
        title_label.pack(pady=(0, 20))
        
        # Selector categorie
        self.category_selector = CategorySelectorComponent(
            main_frame, 
            self.controller.get_available_categories(),
            self._on_category_changed
        )
        self.category_selector.pack(pady=(0, 20))
        
        # Afișare scor
        self.score_display = ScoreDisplayComponent(main_frame)
        self.score_display.pack(pady=(0, 20))
        
        # Afișare cuvânt
        self.word_display = WordDisplayComponent(main_frame)
        self.word_display.pack(pady=20, padx=50, fill='x')
        
        # Afișare status
        self.status_display = StatusDisplayComponent(main_frame)
        self.status_display.pack(pady=10)
        
        # Panou control
        self.control_panel = ControlPanelComponent(
            main_frame,
            on_listen=self._on_listen_clicked,
            on_speak=self._on_speak_clicked,
            on_skip=self._on_skip_clicked,
            on_restart=self._on_restart_clicked
        )
        self.control_panel.pack(pady=20)
        
        # Verifică statusul audio
        self._check_audio_status()
    
    def _setup_controller_callbacks(self) -> None:
        """Configurează callback-urile pentru controller"""
        self.controller.set_callbacks(
            on_word_changed=self._on_word_changed,
            on_score_changed=self._on_score_changed,
            on_status_changed=self._on_status_changed,
            on_feedback_correct=self._on_feedback_correct,
            on_feedback_incorrect=self._on_feedback_incorrect,
            on_listening_changed=self._on_listening_changed,
            on_category_completed=self._on_category_completed
        )
    
    def _initialize_game(self) -> None:
        """Inițializează jocul"""
        default_category = self.category_selector.get_selected()
        if default_category:
            self.controller.start_new_category(default_category)
    
    def _check_audio_status(self) -> None:
        """Verifică și afișează statusul serviciilor audio"""
        status = self.controller.get_audio_status()
        
        warnings = []
        if not status['tts_available']:
            warnings.append("• Serviciul text-to-speech nu este disponibil")
        if not status['stt_available']:
            warnings.append("• Serviciul de recunoaștere vocală nu este disponibil")
        
        if warnings:
            warning_msg = "Avertismente audio:\n" + "\n".join(warnings)
            warning_msg += "\n\nApplicația va funcționa cu funcționalitate limitată."
            messagebox.showwarning("Avertisment Audio", warning_msg)
    
    # Callbacks pentru UI events
    def _on_category_changed(self, category: str) -> None:
        """Callback pentru schimbarea categoriei"""
        self.controller.start_new_category(category)
    
    def _on_listen_clicked(self) -> None:
        """Callback pentru butonul de ascultare"""
        self.controller.start_listening()
    
    def _on_speak_clicked(self) -> None:
        """Callback pentru butonul de pronunțare"""
        self.controller.speak_current_word()
    
    def _on_skip_clicked(self) -> None:
        """Callback pentru butonul de skip"""
        self.controller.skip_current_word()
    
    def _on_restart_clicked(self) -> None:
        """Callback pentru butonul de restart"""
        result = messagebox.askyesno(
            "Restart Categorie", 
            "Ești sigur că vrei să restarți categoria curentă?"
        )
        if result:
            self.controller.restart_current_category()
    
    # Callbacks pentru controller events
    def _on_word_changed(self, word: str) -> None:
        """Callback pentru schimbarea cuvântului"""
        self.word_display.set_word(word)
    
    def _on_score_changed(self, score: int, total: int) -> None:
        """Callback pentru schimbarea scorului"""
        self.score_display.update_score(score, total)
    
    def _on_status_changed(self, status: str) -> None:
        """Callback pentru schimbarea statusului"""
        self.status_display.set_status(status)
    
    def _on_feedback_correct(self) -> None:
        """Callback pentru feedback corect"""
        self.word_display.show_success()
    
    def _on_feedback_incorrect(self) -> None:
        """Callback pentru feedback incorect"""
        self.word_display.blink_error()
    
    def _on_listening_changed(self, is_listening: bool) -> None:
        """Callback pentru schimbarea statusului de ascultare"""
        self.control_panel.set_listening_mode(is_listening)
    
    def _on_category_completed(self, category: str, score: int, total: int, percentage: float) -> None:
        """Callback pentru finalizarea categoriei"""
        message = UIText.COMPLETION_MESSAGE.format(
            category=category, 
            score=score, 
            total=total, 
            percentage=percentage
        )
        
        result = messagebox.askyesno(
            UIText.COMPLETION_TITLE, 
            message + UIText.COMPLETION_QUESTION
        )
        
        if result:
            self.controller.restart_current_category()
        else:
            self.word_display.set_word("Selectează o categorie")
            self.status_display.set_status(UIText.STATUS_SELECT_CATEGORY)
    
    def run(self) -> None:
        """Pornește aplicația"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Aplicația a fost închisă.")
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare neașteptată: {e}")

def main():
    """Funcția principală"""
    try:
        app = SpeechTherapyApp()
        app.run()
    except ImportError as e:
        print("Eroare: Lipsesc biblioteci necesare.")
        print("Instalează cu: pip install speechrecognition pyttsx3 pyaudio")
        print(f"Detalii eroare: {e}")
    except Exception as e:
        print(f"Eroare la pornirea aplicației: {e}")

if __name__ == "__main__":
    main()