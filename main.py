import os
import tkinter as tk
from tkinter import filedialog, ttk
from pytube import YouTube
from threading import Thread
import tkinter.font as tkfont
from PIL import Image, ImageTk

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")

        window_width = 600
        window_height = 260
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

        self.font = tkfont.Font(size=16)

        self.root.configure(bg="#434243")

        self.url_label = tk.Label(root, text="URL:", font=self.font, bg="#434243", fg="#FFFEFE")
        self.url_label.pack(anchor="w", padx=20)

        self.url_entry = tk.Entry(root, font=self.font, bg="#FFFEFE", fg="#434243", insertbackground="#434243")
        self.url_entry.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self.format_label = tk.Label(root, text="Format:", font=self.font, bg="#434243", fg="#FFFEFE")
        self.format_label.pack(anchor="w", padx=20)

        self.format_var = tk.StringVar(value="mp4 720p")
        self.format_combobox = ttk.Combobox(root, textvariable=self.format_var, values=["mp4 144p", "mp4 240p", "mp4 360p", "mp4 480p", "mp4 720p", "mp3"], font=self.font, state="readonly", background="#FFFEFE", foreground="#434243")
        self.format_combobox.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self.download_button = tk.Button(root, text="Download", command=self.start_download, font=self.font, bg="#FFFEFE", fg="#434243")
        self.download_button.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self.progress_label = tk.Label(root, text="", font=self.font, bg="#434243", fg="#FFFEFE")
        self.progress_label.pack()

        self.format_combobox.bind("<FocusIn>", self.adjust_combobox_size)
        self.format_combobox.bind("<FocusOut>", self.reset_combobox_size)

    def adjust_combobox_size(self, event):
        self.format_combobox.config(height=2)

    def reset_combobox_size(self, event):
        self.format_combobox.config(height=1)

    def start_download(self):
        self.url = self.url_entry.get()
        self.video = YouTube(self.url)
        self.format = self.format_var.get()
        self.download_thread = Thread(target=self.download_video)
        self.download_thread.start()

    def download_video(self):
        video_title = self.get_video_title()
        file_extension = self.format.split()[0]
        suggested_filename = f"{video_title}.{file_extension}"

        self.save_path = filedialog.asksaveasfilename(defaultextension=f".{file_extension}", initialfile=suggested_filename, filetypes=[(f"Video files (*.{file_extension})", f"*.{file_extension}")])

        if self.save_path:
            self.video.register_on_progress_callback(self.update_progress)
            self.select_stream(file_extension).download(output_path='.', filename=self.save_path)
            self.progress_label.config(text="Download abgeschlossen")

    def select_stream(self, file_extension):
        if file_extension == "mp3":
            return self.video.streams.filter(only_audio=True).first()
        elif file_extension.startswith("mp4"):
            resolution = self.format.split()[1] if len(self.format.split()) > 1 else None
            return self.get_video_stream_by_resolution(resolution)

    def get_video_stream_by_resolution(self, resolution):
        streams = self.video.streams.filter(file_extension="mp4", resolution=resolution)
        return streams.first()

    def get_video_title(self):
        return self.video.title.replace(" ", "_")

    def update_progress(self, stream, chunk, bytes_remaining):
        file_size = stream.filesize
        bytes_downloaded = file_size - bytes_remaining
        percent = (bytes_downloaded / file_size) * 100
        self.progress_label.config(text=f"{percent:.2f}%")

if __name__ == "__main__":
    root = tk.Tk()

    script_path = os.path.dirname(os.path.abspath(__file__))
    icon_filename = "ytlogo.png"
    icon_path = os.path.join(script_path, icon_filename)

    icon_image = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon_image)

    root.iconphoto(True, icon_photo)

    app = YouTubeDownloader(root)
    root.mainloop()

    
