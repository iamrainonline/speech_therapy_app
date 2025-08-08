# word_manager.py
"""
Manager pentru gestionarea categoriilor de cuvinte
"""
from typing import Dict, List, Optional
from models import WordCategory

class WordCategoryManager:
    """Manager pentru categoriile de cuvinte"""
    
    def __init__(self):
        self._categories = self._load_categories()
    
    def _load_categories(self) -> Dict[str, WordCategory]:
        """Încarcă toate categoriile de cuvinte"""
        categories_data = {
            "Animale": [
                "pisică", "câine", "cal", "vacă", "porc", "oaie", "capră",
                "iepure", "găină", "rață", "gâscă", "leu", "tigru", "elefant",
                "maimuță", "urs", "vulpe", "lup", "șoarece", "pasăre"
            ],
            "Obiecte Casă": [
                "masă", "scaun", "pat", "dulap", "televizor", "frigider",
                "cuptor", "fereastră", "ușă", "oglindă", "canapea", "fotoliu",
                "lampă", "ceas", "carte", "pahar", "farfurie", "lingură", "furculiță", "cuțit"
            ],
            "Corpul Uman": [
                "cap", "față", "ochi", "nas", "gură", "ureche", "păr",
                "gât", "umăr", "braț", "mână", "deget", "piept", "spate",
                "picior", "genunchi", "picior", "deget de la picior", "inimă", "stomac"
            ],
            "Mâncare": [
                "pâine", "lapte", "apă", "mere", "banane", "portocale",
                "roșii", "cartofi", "ceapă", "morcovi", "salată", "carne",
                "pește", "ou", "brânză", "unt", "zahăr", "sare", "orez", "paste"
            ],
            "Culori": [
                "roșu", "albastru", "verde", "galben", "negru", "alb",
                "portocaliu", "violet", "roz", "maro", "gri", "turcoaz"
            ],
            "Familie": [
                "mamă", "tată", "fiu", "fiică", "bunic", "bunică",
                "frate", "soră", "unchi", "mătușă", "verișor", "verișoară",
                "soț", "soție", "copil", "bebeluș", "nepot", "nepoată"
            ],
            "Numere": [
                "unu", "doi", "trei", "patru", "cinci", "șase", "șapte",
                "opt", "nouă", "zece", "unsprezece", "doisprezece"
            ],
            "Verbe Simple": [
                "merg", "vin", "mănânc", "beau", "dorm", "vorbesc",
                "citesc", "scriu", "ascult", "privesc", "iau", "dau"
            ]
        }
        
        return {
            name: WordCategory(name, words) 
            for name, words in categories_data.items()
        }
    
    def get_category_names(self) -> List[str]:
        """Returnează numele tuturor categoriilor"""
        return list(self._categories.keys())
    
    def get_category(self, name: str) -> Optional[WordCategory]:
        """Returnează o categorie specifică"""
        return self._categories.get(name)
    
    def add_category(self, name: str, words: List[str]) -> None:
        """Adaugă o categorie nouă"""
        self._categories[name] = WordCategory(name, words)
    
    def remove_category(self, name: str) -> bool:
        """Șterge o categorie"""
        if name in self._categories:
            del self._categories[name]
            return True
        return False