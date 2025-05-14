import tkinter as tk
from tkinter import ttk, font
import datetime
import socket
import os
import locale

LOG_FILE = "internet_log.txt"

class InternetMonitorApp:
    def __init__(self, root):
        # Set the locale for system date and time format
        locale.setlocale(locale.LC_TIME, '')
        self.root = root
        self.root.title("Internet Monitor")
        self.root.geometry("450x200") # Fixed size
        self.root.resizable(False, False) # Not resizable

        self.is_connected = None
        self.last_down_time = None
        self.last_up_time = None

        self.load_last_events()

        # Styles
        self.bold_font = font.Font(weight="bold", size=16)
        self.status_font_connected = font.Font(weight="bold", size=20)
        self.status_font_disconnected = font.Font(weight="bold", size=20)
        self.button_font = font.Font(size=14) # Added font for the button

        # Main frame
        main_frame = ttk.Frame(root, padding="10 10 10 10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Status message
        self.status_label = ttk.Label(main_frame, text="Verifica in corso...", font=self.status_font_connected, anchor=tk.CENTER)
        self.status_label.pack(pady=10, fill=tk.X)

        # Frame for event information
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=5)

        # Last disconnection
        ttk.Label(info_frame, text="Ultima disconnessione:", font=self.bold_font).grid(row=0, column=0, sticky=tk.W, padx=5)
        self.last_down_label = ttk.Label(info_frame, text="N/A", font=self.bold_font, foreground="red")
        self.last_down_label.grid(row=0, column=1, sticky=tk.E, padx=5)
        if self.last_down_time:
            self.last_down_label.config(text=self.last_down_time.strftime("%x %H:%M"), font=self.bold_font)

        # Last reconnection
        ttk.Label(info_frame, text="Ultima riconnessione:", font=self.bold_font).grid(row=1, column=0, sticky=tk.W, padx=5)
        self.last_up_label = ttk.Label(info_frame, text="N/A", font=self.bold_font, foreground="green")
        self.last_up_label.grid(row=1, column=1, sticky=tk.E, padx=5)
        if self.last_up_time:
            self.last_up_label.config(text=self.last_up_time.strftime("%x %H:%M"), font=self.bold_font)

        info_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(1, weight=1)

        # Close button
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
            # Try to connect to a reliable host (e.g. Google DNS)
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

if __name__ == "__main__":
    root = tk.Tk()
    app = InternetMonitorApp(root)
    root.mainloop()