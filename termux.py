import os
import sys
import yt_dlp

# ========= AYARLAR =========
DOWNLOAD_DIR = os.path.expanduser("~/AHE_MODS")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

LINKS_FILE = os.path.join(DOWNLOAD_DIR, "links.txt")

# ========= FONKSİYONLAR =========
def download_video(url):
    # Kalite ve format seçimi
    print("Kalite seçenekleri: 1080, 720, 480, best")
    quality = input("Kalite seçin (default 'best'): ") or "best"
    if quality == "1080":
        fmt = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
    elif quality == "720":
        fmt = "bestvideo[height<=720]+bestaudio/best[height<=720]"
    elif quality == "480":
        fmt = "bestvideo[height<=480]+bestaudio/best[height<=480]"
    else:
        fmt = "best"

    ext = input("Format seçin (mp4, mkv, webm) [default mp4]: ") or "mp4"
    if ext not in ["mp4","mkv","webm"]:
        ext = "mp4"

    ydl_opts = {
        "format": fmt,
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s - AHE_MODS." + ext),
        "merge_output_format": ext
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("✅ Video indirildi!")
    except Exception as e:
        print(f"❌ Video indirme başarısız: {e}")

def batch_download():
    if not os.path.isfile(LINKS_FILE):
        print(f"❌ {LINKS_FILE} bulunamadı.")
        return

    try:
        with open(LINKS_FILE, "r", encoding="utf-8") as f:
            for url in f:
                url = url.strip()
                if url:
                    ydl_opts = {
                        "format": "best",
                        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s - AHE_MODS.mp4"),
                        "merge_output_format": "mp4"
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
        print("✅ Batch indirme tamamlandı!")
    except Exception as e:
        print(f"❌ Batch indirme hatası: {e}")

# ========= TERMINAL ARAYÜZÜ =========
def main():
    while True:
        print("\nAHE MODS Video Downloader (Termux CLI)")
        print("1. Tek Video İndir")
        print("2. links.txt'den İndir (toplu)")
        print("3. Çıkış")
        choice = input("Seçiminiz: ")

        if choice == "1":
            url = input("Video linkini girin: ")
            if url:
                download_video(url)
        elif choice == "2":
            batch_download()
        elif choice == "3":
            print("Çıkış yapılıyor...")
            sys.exit()
        else:
            print("Geçersiz seçim. Tekrar deneyin.")

if __name__ == "__main__":
    main()