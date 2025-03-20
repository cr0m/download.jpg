import os
import time
import random
import threading
from datetime import datetime
from tkinter import Tk, Button, Label, filedialog, StringVar

# GUI Application
class DirectoryMonitorApp:
    def __init__(self, master):
        self.master = master
        master.title("Directory Monitor")

        self.watch_directory = ""
        self.running = False

        self.dir_label_text = StringVar()
        self.dir_label_text.set("No directory selected")

        self.select_button = Button(master, text="Select Directory", command=self.select_directory)
        self.select_button.pack()

        self.dir_label = Label(master, textvariable=self.dir_label_text)
        self.dir_label.pack()

        self.exit_button = Button(master, text="Exit", command=self.exit_monitoring)
        self.exit_button.pack()

    def select_directory(self):
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.watch_directory = selected_dir
            self.dir_label_text.set(f"Monitoring: {self.watch_directory}")

            if not self.running:
                self.running = True
                threading.Thread(target=self.monitor_and_rename, daemon=True).start()

    def generate_new_filename(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        random_number = random.randint(0, 65535)
        return f"{timestamp}_{random_number:04X}.jpg"

    def monitor_and_rename(self):
        TARGET_FILENAME = 'download.jpg'
        while self.running:
            target_path = os.path.join(self.watch_directory, TARGET_FILENAME)
            if os.path.exists(target_path):
                new_filename = self.generate_new_filename()
                new_filepath = os.path.join(self.watch_directory, new_filename)
                try:
                    os.rename(target_path, new_filepath)
                    print(f"Renamed '{TARGET_FILENAME}' to '{new_filename}'")
                except Exception as e:
                    print(f"Error renaming file: {e}")
            time.sleep(1)

    def exit_monitoring(self):
        self.running = False
        self.master.quit()


if __name__ == "__main__":
    root = Tk()
    app = DirectoryMonitorApp(root)
    root.mainloop()
