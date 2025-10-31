import time
from playwright.sync_api import sync_playwright

def test_opnews_navigation():
    with sync_playwright() as p:
        # 1. Mở trình duyệt Chrome/Chromium
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 2. Mở trang web
        page.goto("https://a.opnews.net/")

        # 3. Cuộn xuống cuối trang
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(3)

        # 4. Tìm card "Data Analytics" và click
        page.get_by_text("Data Analytics", exact=True).click()

        # 5. Chờ vài giây
        time.sleep(3)

        # 6. Click nút "Home" để quay về trang chính
        page.locator("text=Home").first.click()

        # 7. Đóng trình duyệt
        time.sleep(2)
        browser.close()
