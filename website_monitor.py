import threading
import time
import requests
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

class Monitor:
    def __init__(self, url, keywords, interval, output_widget):
        self.url = url
        self.keywords = [k.strip() for k in keywords.split(',') if k.strip()]
        self.interval = interval
        self.output = output_widget
        self._stop_event = threading.Event()
        self.thread = threading.Thread(target=self.run, daemon=True)

    def start(self):
        self.thread.start()

    def stop(self):
        self._stop_event.set()

    def run(self):
        while not self._stop_event.is_set():
            try:
                response = requests.get(self.url, timeout=10)
                text = response.text.lower()
                found = [kw for kw in self.keywords if kw.lower() in text]
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                if found:
                    msg = f"[{timestamp}] Keywords {found} found on {self.url}\n"
                else:
                    msg = f"[{timestamp}] No keywords found on {self.url}\n"
                self.output.configure(state='normal')
                self.output.insert(tk.END, msg)
                self.output.see(tk.END)
                self.output.configure(state='disabled')
            except Exception as e:
                self.output.configure(state='normal')
                self.output.insert(tk.END, f"Error fetching {self.url}: {e}\n")
                self.output.see(tk.END)
                self.output.configure(state='disabled')
            self._stop_event.wait(self.interval)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Website Monitor")
        self.monitors = []
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(padx=10, pady=10)

        ttk.Label(frame, text="Website URL:").grid(column=0, row=0, sticky=tk.W)
        self.url_entry = ttk.Entry(frame, width=50)
        self.url_entry.grid(column=1, row=0, padx=5, pady=2)

        ttk.Label(frame, text="Keywords (comma separated):").grid(column=0, row=1, sticky=tk.W)
        self.keywords_entry = ttk.Entry(frame, width=50)
        self.keywords_entry.grid(column=1, row=1, padx=5, pady=2)

        ttk.Label(frame, text="Interval (seconds):").grid(column=0, row=2, sticky=tk.W)
        self.interval_entry = ttk.Entry(frame, width=20)
        self.interval_entry.grid(column=1, row=2, sticky=tk.W, padx=5, pady=2)
        self.interval_entry.insert(0, "60")

        add_button = ttk.Button(frame, text="Add Monitor", command=self.add_monitor)
        add_button.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)

        self.output = scrolledtext.ScrolledText(self, width=80, height=20, state='disabled')
        self.output.pack(padx=10, pady=10)

    def add_monitor(self):
        url = self.url_entry.get().strip()
        keywords = self.keywords_entry.get().strip()
        try:
            interval = int(self.interval_entry.get().strip())
        except ValueError:
            messagebox.showerror("Invalid interval", "Interval must be an integer number of seconds")
            return
        if not url or not keywords:
            messagebox.showerror("Missing data", "Please provide both URL and keywords")
            return
        monitor = Monitor(url, keywords, interval, self.output)
        monitor.start()
        self.monitors.append(monitor)
        self.url_entry.delete(0, tk.END)
        self.keywords_entry.delete(0, tk.END)

    def on_close(self):
        for m in self.monitors:
            m.stop()
        self.destroy()

if __name__ == '__main__':
    app = App()
    app.mainloop()
