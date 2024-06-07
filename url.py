from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import m3u8

def get_selcuksportshd_streams(url):
    try:
        # Chromedriver'ı başlat (chromedriver'ın PATH'ini doğru ayarladığınızdan emin olun)
        service = Service('chromedriver.exe')  # chromedriver'ın yolunu belirtin
        driver = webdriver.Chrome(service=service)
        driver.get(url)

        # Canlı yayın linklerini bul
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-id]"))
        )
        yayin_linkleri = driver.find_elements(By.CSS_SELECTOR, "a[data-id]")

        streams = []
        for link in yayin_linkleri:
            yayin_url = link.get_attribute("href")

            driver.get(yayin_url)

            # M3U8 URL'sini bul
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "script[src*='.m3u8']"))
            )
            m3u8_url = driver.find_element(By.CSS_SELECTOR, "script[src*='.m3u8']").get_attribute("src")
            print(f"M3U8 URL: {m3u8_url}")

            playlist = m3u8.load(m3u8_url)

            if playlist.is_variant:
                streams.extend([(playlist.playlists[i].stream_info.resolution, playlist.playlists[i].uri) for i in range(len(playlist.playlists))])
            else:
                streams.append((None, m3u8_url))

        driver.quit()  # Tarayıcıyı kapat
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
