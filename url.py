import requests
import m3u8
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

def get_selcuksportshd_streams(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Ana sayfadaki canlı yayın linklerini bulma
        yayin_linkleri = soup.find_all('a', {'data-id': True})  # data-id özelliği olan linkleri bul

        streams = []
        for link in yayin_linkleri:
            yayin_url = link['href']  # Yayın sayfasının URL'si

            response = requests.get(yayin_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Yayın sayfasındaki M3U8 URL'sini bulma
            m3u8_url = soup.find('script', text=lambda t: t and "var player" in t).text
            m3u8_url = m3u8_url.split("file: '")[1].split("'")[0]

            print(f"M3U8 URL: {m3u8_url}")

            m3u8_content = requests.get(m3u8_url).text
            playlist = m3u8.loads(m3u8_content)

            if playlist.is_variant:
                streams.extend([(playlist.playlists[i].stream_info.resolution, playlist.playlists[i].uri) for i in range(len(playlist.playlists))])
            else:
                streams.append((None, m3u8_url))

        return streams

    except (RequestException, KeyError, AttributeError, IndexError, Exception) as e:
        print(f"Hata: {e}")
        return []

url = "https://www.selcuksportshd1274.xyz/"  # Ana sayfa URL'si
streams = get_selcuksportshd_streams(url)

if streams:
    for quality, stream_url in streams:
        if quality:
            print(f"Kalite: {quality[0]}x{quality[1]}, URL: {stream_url}")
        else:
            print(f"Tek Kalite, URL: {stream_url}")
else:
    print("Akış bulunamadı.")