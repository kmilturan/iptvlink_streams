from playwright.sync_api import sync_playwright

def find_yoda_streams():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        streams = set()

        def on_request(request):
            if ".m3u8" in request.url:
                streams.add(request.url)
                print(f"[TAPILDI]: {request.url}")

        page.on("request", on_request)
        
        print("Yoda.az saytına qoşulur...")
        page.goto("https://yoda.az/tv/")
        page.wait_for_timeout(10000)
        browser.close()

        # Tapılan linklərdən .m3u playlist faylı yaradırıq
        m3u_content = "#EXTM3U\n"
        for idx, s in enumerate(streams, 1):
            m3u_content += f'#EXTINF:-1 tvg-name="Kanal {idx}",Kanal {idx}\n'
            m3u_content += f'#EXTVLCOPT:http-referrer=https://yoda.az/\n'
            m3u_content += f'{s}\n'

        with open("yoda_playlist.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("Playlist uğurla yaradıldı!")

if __name__ == "__main__":
    find_yoda_streams()
