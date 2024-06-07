from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By  # By sınıfını import et
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import m3u8
from bs4 import BeautifulSoup
import time

def get_selcuksportshd_streams(url):
    try:
        options = Options()
        options.add_argument("--headless=new")  # Penceresiz modda çalıştır
        options.add_argument("--disable-gpu")   # GPU hızlandırmayı devre dışı bırak
        options.add_argument("--no-sandbox")    # Sandbox modunu devre dışı bırak

        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)

        # Canlı yayın linklerini bul
        yayin_linkleri = driver.find_elements(By.CSS_SELECTOR, "a[data-id]")

        streams = []
        for link in yayin_linkleri:
            yayin_url = link.get_attribute("href")

            driver.get(yayin_url)

            # M3U8 URL'sini bul
            time.sleep(5)  # Sayfanın tamamen yüklenmesi için bekleme
            m3u8_url = driver.find_element(By.CSS_SELECTOR, "script[src*='.m3u8']").get_attribute("src")
            print(f"M3U8 URL: {m3u8_url}")

            playlist = m3u8.load(m3u8_url)

            if playlist.is_variant:
                streams.extend([(playlist.playlists[i].stream_info.resolution, playlist.playlists[i].uri) for i in range(len(playlist.playlists))])
            else:
                streams.append((None, m3u8_url))

        driver.quit()
        return streams

    except Exception as e:
        print(f"Hata: {e}")
        if 'driver' in locals():
            driver.quit()
        return []


url = "https://www.selcuksportshd1274.xyz/"
streams = get_selcuksportshd_streams(url)

if streams:
    for quality, stream_url in streams:
        if quality:
            print(f"Kalite: {quality[0]}x{quality[1]}, URL: {stream_url}")
        else:
            print(f"Tek Kalite, URL: {stream_url}")
else:
    print("Akış bulunamadı.")