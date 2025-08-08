# ui_components.py
"""
Componente pentru interfața utilizatorului
"""
import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Optional
from config import Colors, UIText
import time
import threading

class WordDisplayComponent:
    """Componentă pentru afișarea cuvântului"""
    
    def __init__(self, parent: tk.Widget):
        self.frame = tk.Frame(parent, bg=Colors.WHITE, relief='raised', bd=2)
        self.label = tk.Label(
            self.frame, 
            text="", 
            font=('Arial', 48, 'bold'), 
            bg=Colors.WHITE, 
            fg=Colors.TEXT_PRIMARY, 
            pady=40
        )
        self.label.pack()
    
    def set_word(self, word: str) -> None:
        """Setează cuvântul de afișat"""
        self.label.config(text=word)
        self.reset_appearance()
    
    def reset_appearance(self) -> None:
        """Resetează aspectul la normal"""
        self.frame.config(bg=Colors.WHITE)
        self.label.config(bg=Colors.WHITE, fg=Colors.TEXT_PRIMARY)
    
    def show_success(self) -> None:
        """Afișează feedback de succes"""
        self.frame.config(bg=Colors.SUCCESS_BG)
        self.label.config(bg=Colors.SUCCESS_BG, fg=Colors.SUCCESS_FG)
    
    def blink_error(self, blink_count: int = 3, duration: float = 0.2) -> None:
        """Afișează feedback de eroare cu blink"""
        def blink():
            for _ in range(blink_count):
                self.frame.config(bg=Colors.ERROR_BG)
                self.label.config(bg=Colors.ERROR_BG)
                time.sleep(duration)
                self.reset_appearance()
                time.sleep(duration)
        
        threading.Thread(target=blink, daemon=True).start()
    
    def pack(self, **kwargs) -> None:
        """Pack componenta"""
        self.frame.pack(**kwargs)

class CategorySelectorComponent:
    """Componentă pentru selectarea categoriei"""
    
    def __init__(self, parent: tk.Widget, categories: List[str], 
                 on_change: Callable[[str], None]):
        self.frame = tk.Frame(parent, bg=Colors.BACKGROUND)
        
        tk.Label(
            self.frame, 
            text=UIText.CATEGORY_LABEL, 
            font=('Arial', 14), 
            bg=Colors.BACKGROUND
        ).pack(side='left', padx=(0, 10))
        
        self.var = tk.StringVar(value=categories[0] if categories else "")
        self.combo = ttk.Combobox(
            self.frame, 
            textvariable=self.var,
            values=categories,
            font=('Arial', 12), 
            state='readonly'
        )
        self.combo.pack(side='left')
        self.combo.bind('<<ComboboxSelected>>', lambda e: on_change(self.var.get()))
    
    def get_selected(self) -> str:
        """Returnează categoria selectată"""
        return self.var.get()
    
    def set_selected(self, category: str) -> None:
        """Setează categoria selectată"""
        self.var.set(category)
    
    def pack(self, **kwargs) -> None:
        """Pack componenta"""
        self.frame.pack(**kwargs)

class ScoreDisplayComponent:
    """Componentă pentru afișarea scorului"""
    
    def __init__(self, parent: tk.Widget):
        self.label = tk.Label(
            parent, 
            text=UIText.SCORE_FORMAT.format(score=0, total=0), 
            font=('Arial', 14), 
            bg=Colors.BACKGROUND
        )
    
    def update_score(self, score: int, total: int) -> None:
        """Actualizează scorul afișat"""
        self.label.config(text=UIText.SCORE_FORMAT.format(score=score, total=total))
    
    def pack(self, **kwargs) -> None:
        """Pack componenta"""
        self.label.pack(**kwargs)

class StatusDisplayComponent:
    """Componentă pentru afișarea statusului"""
    
    def __init__(self, parent: tk.Widget):
        self.label = tk.Label(
            parent, 
            text=UIText.STATUS_DEFAULT,
            font=('Arial', 14), 
            bg=Colors.BACKGROUND, 
            fg=Colors.TEXT_SECONDARY
        )
    
    def set_status(self, text: str, color: str = Colors.TEXT_SECONDARY) -> None:
        """Setează textul de status"""
        self.label.config(text=text, fg=color)
    
    def pack(self, **kwargs) -> None:
        """Pack componenta"""
        self.label.pack(**kwargs)

class ButtonComponent:
    """Componentă pentru butoane"""
    
    def __init__(self, parent: tk.Widget, text: str, command: Callable, 
                 bg_color: str = Colors.BUTTON_PRIMARY, font_size: int = 12):
        self.button = tk.Button(
            parent,
            text=text,
            font=('Arial', font_size),
            bg=bg_color,
            fg=Colors.WHITE,
            command=command,
            padx=20,
            pady=10,
            cursor='hand2'
        )
    
    def set_text(self, text: str) -> None:
        """Schimbă textul butonului"""
        self.button.config(text=text)
    
    def set_color(self, bg_color: str) -> None:
        """Schimbă culoarea butonului"""
        self.button.config(bg=bg_color)
    
    def set_enabled(self, enabled: bool) -> None:
        """Activează/dezactivează butonul"""
        state = 'normal' if enabled else 'disabled'
        self.button.config(state=state)
    
    def pack(self, **kwargs) -> None:
        """Pack butonul"""
        self.button.pack(**kwargs)

class ControlPanelComponent:
    """Panou cu butoane de control"""
    
    def __init__(self, parent: tk.Widget, 
                 on_listen: Callable, 
                 on_speak: Callable,
                 on_skip: Callable, 
                 on_restart: Callable):
        self.frame = tk.Frame(parent, bg=Colors.BACKGROUND)
        
        # Buton pentru ascultarea cuvântului
        self.listen_btn = ButtonComponent(
            self.frame, 
            UIText.LISTEN_BUTTON, 
            on_speak,
            Colors.BUTTON_SUCCESS, 
            14
        )
        self.listen_btn.pack(pady=10)
        
        # Buton microfon
        self.mic_btn = ButtonComponent(
            self.frame, 
            UIText.MIC_BUTTON, 
            on_listen,
            Colors.BUTTON_PRIMARY, 
            16
        )
        self.mic_btn.pack(pady=20)
        
        # Frame pentru butoane secundare
        secondary_frame = tk.Frame(self.frame, bg=Colors.BACKGROUND)
        secondary_frame.pack(pady=20)
        
        self.skip_btn = ButtonComponent(
            secondary_frame, 
            UIText.SKIP_BUTTON, 
            on_skip,
            Colors.BUTTON_WARNING
        )
        self.skip_btn.pack(side='left', padx=10)
        
        self.restart_btn = ButtonComponent(
            secondary_frame, 
            UIText.RESTART_BUTTON, 
            on_restart,
            Colors.BUTTON_SECONDARY
        )
        self.restart_btn.pack(side='left', padx=10)
    
    def set_listening_mode(self, is_listening: bool) -> None:
        """Setează modul de ascultare"""
        if is_listening:
            self.mic_btn.set_text(UIText.MIC_LISTENING)
            self.mic_btn.set_color(Colors.BUTTON_DANGER)
        else:
            self.mic_btn.set_text(UIText.MIC_BUTTON)
            self.mic_btn.set_color(Colors.BUTTON_PRIMARY)
    
    def pack(self, **kwargs) -> None:
        """Pack componenta"""
        self.frame.pack(**kwargs)