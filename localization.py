import locale
import json
import os
import sys
import tkinter.messagebox as messagebox

class Localization:
    def __init__(self):
        
        # Determine the base path based on execution mode (script or executable)
        if getattr(sys, 'frozen', False):
            # If running as a compiled executable
            base_path = os.path.dirname(sys.executable)
        else:
            # If running as a Python script
            base_path = os.path.dirname(os.path.abspath(__file__))
            
        self._locales_dir = os.path.join(base_path, "locales")  # Localization directory path
        self.translations = {}
        self.current_language = "en"  # Default language
        self.available_languages = []
        
        # Discover available languages from locales directory
        self._discover_available_languages()
        
        # Load all available language files
        self._load_languages()
        
        # Set initial language based on system settings
        self.set_language_from_system()
    
    def _discover_available_languages(self):
        """Discover available languages from embedded resources or locales directory"""
        # Default languages that are always available
        self.available_languages = ["en", "it"]
        
        # Check for additional language files in locales directory
        # This works for both normal script and frozen executable
        if not os.path.exists(self._locales_dir):
            # Try to create directory if running as script
            if not getattr(sys, 'frozen', False):
                os.makedirs(self._locales_dir)
            return
            
        # Scan directory for additional language files
        try:
            files = os.listdir(self._locales_dir)
            for file in files:
                if file.endswith(".json"):
                    lang_code = file.split(".")[0]
                    if lang_code not in self.available_languages:
                        self.available_languages.append(lang_code)
        except Exception as e:
            error_msg = f"Error scanning languages directory: {e}"
            print(error_msg)
            messagebox.showerror("Error", error_msg) # Show error in GUI
    
    def _load_languages(self):
        """Load all available language files from embedded resources or locales directory"""
        # Load embedded language data first
        self._load_embedded_languages()
        
        # When running as a normal script, create directory and default files if needed
        if not getattr(sys, 'frozen', False):
            if not os.path.exists(self._locales_dir):
                os.makedirs(self._locales_dir)
                
            # Create language files if they don't exist
            for lang in ["en", "it"]:
                lang_file = os.path.join(self._locales_dir, f"{lang}.json")
                if not os.path.exists(lang_file):
                    if lang == "en":
                        self._create_english_file(lang_file)
                    elif lang == "it":
                        self._create_italian_file(lang_file)
        
        # For both script and frozen executable, load language files if they exist
        if os.path.exists(self._locales_dir):
            # Load each language file (will override embedded translations if exists)
            for lang in self.available_languages:
                lang_file = os.path.join(self._locales_dir, f"{lang}.json")
                if os.path.exists(lang_file):
                    try:
                        with open(lang_file, 'r', encoding='utf-8') as f:
                            self.translations[lang] = json.load(f)
                    except Exception as e:
                        error_msg = f"Error loading language file {lang_file}: {e}"
                        print(error_msg)
                        messagebox.showerror("Error", error_msg) # Show error in GUI
    
    def _load_embedded_languages(self):
        """Load embedded language data"""
        # English strings
        self.translations["en"] = {
            "app_title": "Internet Monitor",
            "checking": "Checking connection...",
            "connected": "Connected to Internet",
            "disconnected": "NOT CONNECTED TO INTERNET!",
            "last_disconnection": "Last disconnection:",
            "last_reconnection": "Last reconnection:",
            "close_button": "Close",
            "not_available": "N/A",
            "language_menu": "Language",
            "english": "English",
            "italian": "Italian",
            "autostart_menu": "Autostart",
            "autostart_option": "Start with Windows",
            "open_log_tooltip": "Open log file",
            "log_file_not_found": "Log file not found",
            "delete_log_tooltip": "Delete log file",
            "delete_log_confirm": "Are you sure you want to delete the log file?",
            "delete_log_success": "Log file deleted successfully",
            "delete_log_error": "Error deleting log file: {0}",
            # Error messages
            "error_scanning_locales_dir": "Error scanning locales directory: {0}",
            "error_loading_language_file": "Error loading language file {0}: {1}",
            "error_detecting_system_language": "Error detecting system language: {0}"
        }
        
        # Italian strings
        self.translations["it"] = {
            "app_title": "Internet Monitor",
            "checking": "Verifica in corso...",
            "connected": "Connesso a Internet",
            "disconnected": "NON CONNESSO A INTERNET!",
            "last_disconnection": "Ultima disconnessione:",
            "last_reconnection": "Ultima riconnessione:",
            "close_button": "Chiudi",
            "not_available": "N/A",
            "language_menu": "Lingua",
            "english": "Inglese",
            "italian": "Italiano",
            "autostart_menu": "Avvio automatico",
            "autostart_option": "Avvia con Windows",
            "open_log_tooltip": "Apri file di log",
            "log_file_not_found": "File di log non trovato",
            "delete_log_tooltip": "Elimina file di log",
            "delete_log_confirm": "Sei sicuro di voler eliminare il file di log?",
            "delete_log_success": "File di log eliminato con successo",
            "delete_log_error": "Errore durante l'eliminazione del file di log: {0}",
            # Error messages
            "error_scanning_locales_dir": "Errore durante la scansione della directory delle lingue: {0}",
            "error_loading_language_file": "Errore durante il caricamento del file di lingua {0}: {1}",
            "error_detecting_system_language": "Errore durante il rilevamento della lingua di sistema: {0}"
        }
    
    def _create_english_file(self, file_path):
        """Create the default English language file"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.translations["en"], f, ensure_ascii=False, indent=4)
    
    def _create_italian_file(self, file_path):
        """Create the default Italian language file"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.translations["it"], f, ensure_ascii=False, indent=4)
    
    def set_language(self, lang_code):
        """Set the current language"""
        if lang_code in self.available_languages:
            self.current_language = lang_code
            return True
        return False
    
    def set_language_from_system(self):
        """Set language based on system locale"""
        try:
            # Get the system locale
            system_locale = locale.getdefaultlocale()[0]
            if system_locale:
                # Extract language code (first 2 characters)
                lang_code = system_locale.split('_')[0].lower()
                
                # Check if this language is available
                if lang_code in self.available_languages:
                    self.current_language = lang_code
                    return
            
            # Default to English if system language is not available
            self.current_language = "en"
        except Exception as e:
            error_msg = f"Error detecting system language: {e}"
            print(error_msg)
            messagebox.showerror("Error", error_msg) # Show error in GUI
            self.current_language = "en"
    
    def get_string(self, key, lang_code=None):
        """Get a localized string by key"""
        language = lang_code if lang_code else self.current_language
        try:
            return self.translations[language].get(key, key)
        except:
            # Fallback to English if the current language doesn't have this key
            try:
                return self.translations["en"].get(key, key)
            except:
                # Return the key itself if all else fails
                return key
    
    def get_current_language(self):
        """Get the current language code"""
        return self.current_language
    
    def get_available_languages(self):
        """Get list of available languages"""
        return self.available_languages
        
    def get_localized_error(self, key, *args):
        """Get a localized error message with formatted arguments"""
        # Try to get the error message in English first (as a fallback)
        error_template = ""
        try:
            if "en" in self.translations:
                error_template = self.translations["en"].get(key, key)
        except:
            error_template = key
            
        # Then try to get it in the current language
        try:
            if self.current_language in self.translations:
                error_template = self.translations[self.current_language].get(key, error_template)
        except:
            pass  # Keep the English version or key if we can't get the localized version
            
        # Format the error message with the provided arguments
        try:
            return error_template.format(*args)
        except:
            # If formatting fails, return the template and arguments separately
            return f"{error_template} - {args}"