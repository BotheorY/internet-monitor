import tkinter as tk
from tkinter import ttk, font
import datetime
import socket
import os
import locale

LOG_FILE = "internet_log.txt"

class InternetMonitorApp:
    def __init__(self, root):
        # Imposta il locale per il formato di data e ora del sistema
        locale.setlocale(locale.LC_TIME, '')
        self.root = root
        self.root.title("Internet Monitor")
        self.root.geometry("450x200") # Dimensioni fisse
        self.root.resizable(False, False) # Non ridimensionabile

        self.is_connected = None
        self.last_down_time = None
        self.last_up_time = None

        self.load_last_events()

        # Stili
        self.bold_font = font.Font(weight="bold", size=16)
        self.status_font_connected = font.Font(weight="bold", size=20)
        self.status_font_disconnected = font.Font(weight="bold", size=20)
        self.button_font = font.Font(size=14) # Aggiunto font per il pulsante

        # Frame principale
        main_frame = ttk.Frame(root, padding="10 10 10 10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Messaggio di stato
        self.status_label = ttk.Label(main_frame, text="Verifica in corso...", font=self.status_font_connected, anchor=tk.CENTER)
        self.status_label.pack(pady=10, fill=tk.X)

        # Frame per informazioni eventi
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=5)

        # Ultima disconnessione
        ttk.Label(info_frame, text="Ultima disconnessione:", font=self.bold_font).grid(row=0, column=0, sticky=tk.W, padx=5)
        self.last_down_label = ttk.Label(info_frame, text="N/A", font=self.bold_font, foreground="red")
        self.last_down_label.grid(row=0, column=1, sticky=tk.E, padx=5)
        if self.last_down_time:
            self.last_down_label.config(text=self.last_down_time.strftime("%x %H:%M"), font=self.bold_font)

        # Ultima riconnessione
        ttk.Label(info_frame, text="Ultima riconnessione:", font=self.bold_font).grid(row=1, column=0, sticky=tk.W, padx=5)
        self.last_up_label = ttk.Label(info_frame, text="N/A", font=self.bold_font, foreground="green")
        self.last_up_label.grid(row=1, column=1, sticky=tk.E, padx=5)
        if self.last_up_time:
            self.last_up_label.config(text=self.last_up_time.strftime("%x %H:%M"), font=self.bold_font)

        info_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(1, weight=1)

        # Pulsante Chiudi
        style = ttk.Style()
        style.configure("Large.TButton", font=self.button_font)
        close_button = ttk.Button(main_frame, text="Chiudi", command=self.root.quit, style="Large.TButton")
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
            # Prova a connettersi a un host affidabile (es. Google DNS)
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False

    def update_status(self, connected):
        if connected:
            self.status_label.config(text="Connesso a Internet", foreground="green", font=self.status_font_connected)
        else:
            self.status_label.config(text="NON CONNESSO A INTERNET!", foreground="red", font=self.status_font_disconnected)

    def check_connection(self):
        currently_connected = self.check_internet_connection()

        if self.is_connected is None: # Primo controllo
            self.is_connected = currently_connected
            self.update_status(self.is_connected)
            if not self.is_connected:
                 # Se al primo avvio non c'è connessione e non c'è un evento DOWN precedente, loggalo
                if self.last_down_time is None or (self.last_up_time and self.last_up_time > self.last_down_time):
                    self.log_event("DOWN")
            else:
                # Se al primo avvio c'è connessione e l'ultimo evento è stato DOWN, logga UP
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
            # Lo stato non è cambiato, aggiorna solo il testo se necessario (es. al primo avvio)
            self.update_status(self.is_connected)

        # Pianifica il prossimo controllo tra 60 secondi
        self.root.after(60000, self.check_connection)

if __name__ == "__main__":
    root = tk.Tk()
    app = InternetMonitorApp(root)
    root.mainloop()