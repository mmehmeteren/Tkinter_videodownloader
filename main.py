import os
import tkinter as tk
from tkinter import messagebox, simpledialog
import yt_dlp

# ========= AYARLAR =========
DOWNLOAD_DIR = "/storage/emulated/0/AHE_MODS"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ========= FONKSIYONLAR =========
def download_video():
    url = simpledialog.askstring("Video Linki", "Video linkini yapistir:")
    if not url:
        return

    # Kalite secimi
    quality = simpledialog.askstring("Kalite", "Kalite sec (1080, 720, 480, best):", initialvalue="best")
    if quality == "1080":
        fmt = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
    elif quality == "720":
        fmt = "bestvideo[height<=720]+bestaudio/best[height<=720]"
    elif quality == "480":
        fmt = "bestvideo[height<=480]+bestaudio/best[height<=480]"
    else:
        fmt = "best"

    # Format secimi
    ext = simpledialog.askstring("Format", "Format sec (mp4, mkv, webm):", initialvalue="mp4")
    if ext not in ["mp4", "mkv", "webm"]:
        ext = "mp4"

    ydl_opts = {
        "format": fmt,
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s - AHE MODS." + ext),
        "merge_output_format": ext
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Basarili", "Video indirildi!")
    except Exception as e:
        messagebox.showerror("Hata", f"Video indirme basarisiz!\n{str(e)}")

def batch_download():
    if not os.path.isfile("/storage/emulated/0/AHE_MODS/links.txt"):
        messagebox.showwarning("Uyari", "links.txt bulunamadi.")
        return

    try:
        with open("/storage/emulated/0/AHE_MODS/links.txt", "r") as f:
            for url in f:
                url = url.strip()
                if url:
                    ydl_opts = {
                        "format": "best",
                        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s - AHE MODS.mp4"),
                        "merge_output_format": "mp4"
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
        messagebox.showinfo("Basarili", "Batch indirme tamamlandi!")
    except Exception as e:
        messagebox.showerror("Hata", f"Batch indirme hatasi!\n{str(e)}")

# ========= ARAYUZ =========
root = tk.Tk()
root.title("AHE MODS Video Downloader")
root.geometry("400x250")
root.config(bg="black")

title_label = tk.Label(root, text="AHE MODS Video Downloader", fg="cyan", bg="black", font=("Arial", 16, "bold"))
title_label.pack(pady=15)

btn_video = tk.Button(root, text="Tek Video Indir", command=download_video, font=("Arial", 12), bg="blue", fg="white")
btn_video.pack(pady=10, fill="x")

btn_batch = tk.Button(root, text="links.txt'den Indir", command=batch_download, font=("Arial", 12), bg="orange", fg="black")
btn_batch.pack(pady=10, fill="x")

btn_exit = tk.Button(root, text="Cikis", command=root.quit, font=("Arial", 12), bg="red", fg="white")
btn_exit.pack(pady=10, fill="x")

root.mainloop()