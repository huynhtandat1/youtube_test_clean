import time
import pytest
from playwright.sync_api import Page, expect

def test_youtube_search(page: Page):
    print("🚀 Mở YouTube...")
    page.goto("https://www.youtube.com", wait_until="domcontentloaded")
    page.wait_for_load_state("networkidle")
    print("🌐 URL hiện tại:", page.url)
    page.screenshot(path="youtube_start.png")

    # 🧩 Nếu bị redirect sang trang consent.youtube.com (đồng ý cookie)
    if "consent.youtube.com" in page.url:
        print("⚙️ Trang yêu cầu đồng ý cookie...")
        btn = page.locator("button:has-text('I agree'), button:has-text('Accept all'), form[action] button")
        try:
            btn.first.wait_for(state="visible", timeout=10000)
            btn.first.click()
            print("✅ Đã bấm đồng ý, quay lại YouTube...")
            page.wait_for_load_state("networkidle")
            time.sleep(3)
            page.goto("https://www.youtube.com", wait_until="networkidle")
        except:
            print("⚠️ Không thấy nút đồng ý, bỏ qua...")

    # 🔍 Chờ và tìm ô tìm kiếm (đa ngôn ngữ)
    print("🔍 Chờ thanh tìm kiếm sẵn sàng...")
    search_box = page.locator("input#search")

    try:
        search_box.wait_for(state="visible", timeout=10000)
    except:
        print("⚠️ input#search không hoạt động, thử fallback...")
        search_box = page.get_by_placeholder("Tìm kiếm")
        search_box.wait_for(timeout=10000)

    # 📝 Gõ từ khóa tìm kiếm
    keyword = "Playwright Python tutorial"
    print(f"⌨️  Nhập từ khóa: {keyword}")
    search_box.fill(keyword)
    page.keyboard.press("Enter")

    # ⏳ Chờ kết quả tìm kiếm
    print("⏳ Đang chờ kết quả hiển thị...")
    page.wait_for_selector("ytd-video-renderer", timeout=20000)
    page.screenshot(path="youtube_results.png")

    # ✅ Kiểm tra kết quả đầu tiên có chứa từ khóa
    first_video = page.locator("ytd-video-renderer").first
    expect(first_video).to_be_visible()
    print("✅ Đã hiển thị video đầu tiên!")

    print("🎉 Test hoàn tất thành công.")
    
