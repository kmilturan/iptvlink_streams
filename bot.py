from playwright.sync_api import sync_playwright

def find_yoda_api():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        def handle_response(response):
            url = response.url
            # API və ya manifest sorğularını yoxlayırıq
            if "api" in url or ".m3u8" in url or "json" in url:
                print(f"[CAVAB TAPILDI]: {url}")
                try:
                    # Əgər JSON cavabıdırsa, məzmununu oxumağa çalışırıq
                    if "application/json" in response.headers.get("content-type", ""):
                        print("JSON Məlumatı:", response.json())
                except:
                    pass

        page.on("response", handle_response)
        
        print("Yoda.az yoxlanılır...")
        page.goto("https://yoda.az/tv/")
        
        # Kanalların yüklənməsi üçün gözləyirik
        page.wait_for_timeout(10000)
        browser.close()

if __name__ == "__main__":
    find_yoda_api()
