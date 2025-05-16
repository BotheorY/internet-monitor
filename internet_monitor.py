import tkinter as tk
from tkinter import ttk, font
import datetime
import socket
import os
import sys
import locale
from localization import Localization

LOG_FILE = "internet_log.txt"

class InternetMonitorApp:
    def __init__(self, root: tk.Tk):
        # Set the locale for system date and time format
        locale.setlocale(locale.LC_TIME, '')
        
        # Initialize localization
        self.localization = Localization()
        
        self.root = root
        self.root.title(self.localization.get_string("app_title"))
        self.root.geometry("450x220") # Fixed size
        self.root.resizable(False, False) # Not resizable

        # Determine base path for resources
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # If the application is run as a bundle (e.g., by PyInstaller)
            base_path = sys._MEIPASS
        else:
            # If the application is run as a normal Python script
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        icon_path = os.path.join(base_path, 'icon', 'internet-monitor.ico')
        self.root.iconbitmap(icon_path)

        self.is_connected = None
        self.last_down_time = None
        self.last_up_time = None

        self.load_last_events()

        # Styles
        self.bold_font = font.Font(weight="bold", size=16)
        self.status_font_connected = font.Font(weight="bold", size=20)
        self.status_font_disconnected = font.Font(weight="bold", size=20)
        self.button_font = font.Font(size=14) # Added font for the button

        # Create menu bar
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)
        
        # Language menu - creazione dinamica del menu delle lingue
        self.language_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=self.localization.get_string("language_menu"), menu=self.language_menu)
        
        # Add a menu item for each available language
        for lang_code in self.localization.get_available_languages():
            # Get the localized name of the language
            lang_name = self.localization.get_string(lang_code)
            # If the language name is not available, use the language code
            if lang_name == lang_code:
                # Try to get the language name from the English translation
                lang_name = self.localization.get_string(lang_code, "en")
                if lang_name == lang_code:
                    # If still not available, use the language code with the first letter capitalized
                    lang_name = lang_code.capitalize()
            
            # Add a checkmark (✓) next to the currently selected language
            if lang_code == self.localization.get_current_language():
                lang_name = "✓ " + lang_name
            
            # Add the menu item with lambda function for language change
            self.language_menu.add_command(label=lang_name, command=lambda code=lang_code: self.change_language(code))
        
        # Main frame
        main_frame = ttk.Frame(root, padding="10 10 10 10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Status message
        self.status_label = ttk.Label(main_frame, text=self.localization.get_string("checking"), font=self.status_font_connected, anchor=tk.CENTER)
        self.status_label.pack(pady=10, fill=tk.X)

        # Frame for event information
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=5)

        # Last disconnection
        ttk.Label(info_frame, text=self.localization.get_string("last_disconnection"), font=self.bold_font).grid(row=0, column=0, sticky=tk.W, padx=5)
        self.last_down_label = ttk.Label(info_frame, text=self.localization.get_string("not_available"), font=self.bold_font, foreground="red")
        self.last_down_label.grid(row=0, column=1, sticky=tk.E, padx=5)
        if self.last_down_time:
            self.last_down_label.config(text=self.last_down_time.strftime("%x %H:%M"), font=self.bold_font)

        # Last reconnection
        ttk.Label(info_frame, text=self.localization.get_string("last_reconnection"), font=self.bold_font).grid(row=1, column=0, sticky=tk.W, padx=5)
        self.last_up_label = ttk.Label(info_frame, text=self.localization.get_string("not_available"), font=self.bold_font, foreground="green")
        self.last_up_label.grid(row=1, column=1, sticky=tk.E, padx=5)
        if self.last_up_time:
            self.last_up_label.config(text=self.last_up_time.strftime("%x %H:%M"), font=self.bold_font)

        info_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(1, weight=1)

        # Close button
        style = ttk.Style()
        style.configure("Large.TButton", font=self.button_font)
        close_button = ttk.Button(main_frame, text=self.localization.get_string("close_button"), command=self.root.quit, style="Large.TButton")
        close_button.pack(side=tk.BOTTOM, anchor=tk.SE, pady=10, padx=10)

        self.check_connection()

    def log_event(self, event_type):
        timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp} - {event_type}\n")
        if event_type == "DOWN":
            self.last_down_time = datetime.datetime.now()
            self.last_down_label.config(text=self.last_down_time.strftime("%x %H:%M"))
        elif event_type == "UP":
            self.last_up_time = datetime.datetime.now()
            self.last_up_label.config(text=self.last_up_time.strftime("%x %H:%M"))

    def load_last_events(self):
        if not os.path.exists(LOG_FILE):
            return

        last_down = None
        last_up = None
        try:
            with open(LOG_FILE, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(" - ")
                    if len(parts) == 2:
                        try:
                            timestamp_str, event = parts
                            dt_obj = datetime.datetime.strptime(timestamp_str, "%Y/%m/%d %H:%M")
                            if event == "DOWN":
                                if last_down is None or dt_obj > last_down:
                                    last_down = dt_obj
                            elif event == "UP":
                                if last_up is None or dt_obj > last_up:
                                    last_up = dt_obj
                        except ValueError:
                            print(f"Skipping malformed log line: {line}") # Log to console for debugging
                            continue # Skip malformed lines
            self.last_down_time = last_down
            self.last_up_time = last_up
        except Exception as e:
            print(f"Error loading log file: {e}") # Log to console for debugging

    def check_internet_connection(self):
        try:
            # Try to connect to a reliable host (e.g. Google DNS)
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False

    def update_status(self, connected):
        if connected:
            self.status_label.config(text=self.localization.get_string("connected"), foreground="green", font=self.status_font_connected)
        else:
            self.status_label.config(text=self.localization.get_string("disconnected"), foreground="red", font=self.status_font_disconnected)

    def check_connection(self):
        currently_connected = self.check_internet_connection()

        if self.is_connected is None: # First check
            self.is_connected = currently_connected
            self.update_status(self.is_connected)
            if not self.is_connected:
                 # If at first start there is no connection and there is no previous DOWN event, log it
                if self.last_down_time is None or (self.last_up_time and self.last_up_time > self.last_down_time):
                    self.log_event("DOWN")
            else:
                # If at first start there is connection and the last event was DOWN, log UP
                if self.last_down_time and (self.last_up_time is None or self.last_down_time > self.last_up_time):
                    self.log_event("UP")

        elif currently_connected and not self.is_connected:
            self.log_event("UP")
            self.is_connected = True
            self.update_status(True)
        elif not currently_connected and self.is_connected:
            self.log_event("DOWN")
            self.is_connected = False
            self.update_status(False)
        else:
            # The state has not changed, just update the text if necessary (e.g. at first start)
            self.update_status(self.is_connected)

        # Schedule the next check in 60 seconds
        self.root.after(60000, self.check_connection)

    def change_language(self, lang_code):
        """Change the application language"""
        if self.localization.set_language(lang_code):
            # Update all UI text elements
            self.root.title(self.localization.get_string("app_title"))
            
            # Update the status label with the correct localized text
            if self.is_connected is None:
                self.status_label.config(text=self.localization.get_string("checking"))
            else:
                self.status_label.config(text=self.localization.get_string("connected" if self.is_connected else "disconnected"))
            
            # Completely recreate the menu instead of updating it
            # Remove all existing menus
            if self.menu_bar.index("end") is not None:
                self.menu_bar.delete(0, tk.END)
            
            # Dynamically recreate the language menu based on available languages
            self.language_menu = tk.Menu(self.menu_bar, tearoff=0)
            self.menu_bar.add_cascade(label=self.localization.get_string("language_menu"), menu=self.language_menu)
            
            # Add a menu item for each available language
            for lang_code_item in self.localization.get_available_languages():
                # Get the localized name of the language
                lang_name = self.localization.get_string(lang_code_item)
                # If the language name is not available, use the language code
                if lang_name == lang_code_item:
                    # Try to get the language name from the English translation
                    lang_name = self.localization.get_string(lang_code_item, "en")
                    if lang_name == lang_code_item:
                        # If still not available, use the language code with the first letter capitalized
                        lang_name = lang_code_item.capitalize()
                
                # Add a checkmark (✓) next to the currently selected language
                if lang_code_item == self.localization.get_current_language():
                    lang_name = "✓ " + lang_name
                
                # Add the menu item with lambda function for language change
                self.language_menu.add_command(label=lang_name, command=lambda code=lang_code_item: self.change_language(code))
            
            # Update all user interface elements
            self._update_all_ui_elements()
            
    def _update_all_ui_elements(self):
        """Update all user interface elements with localized text"""
        # Use a recursive approach to update all widgets
        self._update_widget_recursive(self.root)
        
        # Update dynamic labels with correct values
        if self.last_down_time:
            self.last_down_label.config(text=self.last_down_time.strftime("%x %H:%M"))
        else:
            self.last_down_label.config(text=self.localization.get_string("not_available"))
            
        if self.last_up_time:
            self.last_up_label.config(text=self.last_up_time.strftime("%x %H:%M"))
        else:
            self.last_up_label.config(text=self.localization.get_string("not_available"))
    
    def _update_widget_recursive(self, widget):
        """Recursively update all user interface widgets"""
        # Update the current widget if it's a type that can contain text
        if isinstance(widget, ttk.Label):
            # Ignore dynamic labels that are updated separately
            if widget not in [self.status_label, self.last_down_label, self.last_up_label]:
                self._update_label_text(widget)
        elif isinstance(widget, ttk.Button):
            # Update the button text
            if widget.cget("text"):
                widget.config(text=self.localization.get_string("close_button"))
        elif isinstance(widget, tk.Menu):
            # Menus have already been recreated in the change_language method
            pass
        
        # Proceed recursively with child widgets
        try:
            children = widget.winfo_children()
            for child in children:
                self._update_widget_recursive(child)
        except (AttributeError, tk.TclError):
            # Some widgets might not have the winfo_children method
            pass
    
    def _update_label_text(self, label):
        """Update a label's text based on the localization key"""
        try:
            # Get the current label text
            current_text = label.cget("text")
            
            # Try to identify the localization key based on widget position
            # Get the parent and position of the widget
            parent = label.master
            if parent and isinstance(parent, ttk.Frame):
                # Try to get the widget position in the grid
                try:
                    # grid_info must be called on the widget itself, not on the parent
                    info = label.grid_info()
                    # If it's in the first column (0) and first row (0), it's the "last_disconnection" label
                    if info.get('column') == '0' and info.get('row') == '0':
                        label.config(text=self.localization.get_string("last_disconnection"))
                        return
                    # If it's in the first column (0) and second row (1), it's the "last_reconnection" label
                    elif info.get('column') == '0' and info.get('row') == '1':
                        label.config(text=self.localization.get_string("last_reconnection"))
                        return
                except (tk.TclError, KeyError):
                    pass  # Not a grid widget or has no grid information
            
            # If it wasn't possible to identify the widget based on position,
            # try to identify it based on current text
            # Check all possible translations of "last_disconnection" and "last_reconnection"
            for lang in self.localization.get_available_languages():
                # Check if the current text matches a translation of "last_disconnection"
                disconnection_text = self.localization.get_string("last_disconnection", lang)
                if disconnection_text == current_text:
                    label.config(text=self.localization.get_string("last_disconnection"))
                    return
                
                # Check if the current text matches a translation of "last_reconnection"
                reconnection_text = self.localization.get_string("last_reconnection", lang)
                if reconnection_text == current_text:
                    label.config(text=self.localization.get_string("last_reconnection"))
                    return
        except (tk.TclError, AttributeError):
            # Ignore errors if the widget doesn't have the text attribute
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = InternetMonitorApp(root)
    root.mainloop()