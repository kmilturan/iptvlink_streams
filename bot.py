import time
from playwright.sync_api import sync_playwright

def generate_yoda_playlist():
    with sync_playwright() as p:
        # Brauzeri işə salırıq
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        channels_data = {}

        # Şəbəkə sorğularını izləyirik ki, hansı linkin hansı `.m3u8` olduğuna baxaq
        def on_request(request):
            if ".m3u8" in request.url:
                # İştirak edən cari URL-i və ya kanal sorğusunu tuturuq
                print(f"[TAPILDI AXIN]: {request.url}")

        page.on("request", on_request)
        
        print("Yoda.az saytına daxil olunur...")
        page.goto("https://yoda.az/tv/")
        
        # Səhifənin və kanalların tam yüklənməsi üçün bir az gözləyirik
        page.wait_for_timeout(5000)

        # Səhifədəki bütün kanal düymələrini/linklərini tapırıq
        # (Saytın strukturuna uyğun olaraq bütün kliklənə bilən kanal elementlərini seçirik)
        channel_elements = page.locator("a.channel-item, .channels-list a, .tv-channels a, [href*='/tv/']").all()
        
        if not channel_elements:
            # Alternativ olaraq səhifədəki bütün tv keçidlərini yoxlayırıq
            channel_elements = page.locator("a").all()

        print(f"Toplandı: {len(channel_elements)} mümkünkanal elementi.")

        # İndi isə hər kanalın üzərinə klikləyib axın linkini tutmağa çalışacağıq
        # (Əgər düymələr çoxdursa, ilk mərhələdə əsas kanalları gəzirik)
        
        browser.close()

if __name__ == "__main__":
    generate_yoda_playlist()
