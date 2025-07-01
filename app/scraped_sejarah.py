import requests
from bs4 import BeautifulSoup
import os

# Fungsi scraping satu URL
def scrape_url(url: str) -> str:
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        text = "\n".join(p.get_text() for p in soup.find_all("p") if len(p.get_text()) > 50)
        return text.strip()
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

# Fungsi scraping banyak URL dan simpan ke file
def scrape_and_save_to_folder(url_file="urls.txt", folder="app/scraped_data"):
    os.makedirs(folder, exist_ok=True)

    with open(url_file, "r") as f:
        urls = f.read().splitlines()

    for i, url in enumerate(urls):
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")

            # Ambil semua isi <p> yang cukup panjang
            text = "\n".join(p.get_text() for p in soup.find_all("p") if len(p.get_text()) > 50)
            if not text.strip():
                print(f"[{i}] Kosong dari: {url}")
                continue

            filename = f"artikel_{i+1}.txt"
            path = os.path.join(folder, filename)

            with open(path, "w", encoding="utf-8") as out:
                out.write(f"# Source: {url}\n\n{text}")
            print(f"[{i}] Sukses simpan: {filename}")

        except Exception as e:
            print(f"[{i}] Gagal scraping {url}: {e}")

if __name__ == "__main__":
    scrape_and_save_to_folder()