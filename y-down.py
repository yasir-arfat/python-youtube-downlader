import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
import yt_dlp
import threading

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        
        self.url_label = tk.Label(root, text="Video URL:")
        self.url_label.grid(row=0, column=0, padx=10, pady=10)
        self.url_labe2 = tk.Label(root, text="by: yasir arfat")
        self.url_labe2.grid(row=1, column=0, padx=10, pady=10,)
                
        
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Create a context menu for the entry widget
        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="Paste", command=self.paste)
        
        # Bind right-click to the entry widget to show context menu
        self.url_entry.bind("<Button-3>", self.show_context_menu)
        
        self.download_button = tk.Button(root, text="Download", command=self.start_download_thread)
        self.download_button.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.progress = Progressbar(root, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.save_path = ""
    
    def select_save_path(self):
        self.save_path = filedialog.askdirectory()
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes', 0)
            downloaded_bytes = d.get('downloaded_bytes', 0)
            if total_bytes > 0:
                progress_percent = (downloaded_bytes / total_bytes) * 100
                self.progress['value'] = progress_percent
                self.root.update_idletasks()
        elif d['status'] in ('finished', 'error'):
            self.progress['value'] = 0
    
    def start_download_thread(self):
        threading.Thread(target=self.download_video).start()
    
    def download_video(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a video URL.")
            return
        
        if not self.save_path:
            self.select_save_path()
        
        if not self.save_path:
            messagebox.showerror("Error", "Please select a save directory.")
            return
        
        try:
            ydl_opts = {
                'outtmpl': f'{self.save_path}/%(title)s.%(ext)s',
                'progress_hooks': [self.progress_hook]
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            messagebox.showinfo("Success", "Video downloaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.progress['value'] = 0
    
    def paste(self):
        try:
            # Get the text from the clipboard
            clipboard_text = self.root.clipboard_get()
            self.url_entry.insert(tk.END, clipboard_text)
        except tk.TclError:
            pass  # Handle empty clipboard case
    
    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

def main():
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()