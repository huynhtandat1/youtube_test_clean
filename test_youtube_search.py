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

    # 🔍 Chờ và tìm ô tìm kiếm
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

    # ✅ Kiểm tra và click video đầu tiên
    first_video = page.locator("ytd-video-renderer").first
    expect(first_video).to_be_visible()
    print("✅ Đã hiển thị video đầu tiên! Bắt đầu xem video...")

    # ▶️ Click vào video đầu tiên
    first_video.click()
    page.wait_for_load_state("networkidle")
    page.screenshot(path="youtube_video_opened.png")

    # 🎬 Chờ video phát
    print("🎬 Đang xem video...")

    # 👉 Nếu muốn chờ đến khi video kết thúc (ví dụ theo thời lượng hiển thị)
    try:
        # Lấy thời lượng video (nếu có)
        duration_text = page.locator("span.ytp-time-duration").inner_text(timeout=10000)
        print(f"⏱️ Thời lượng video: {duration_text}")

        # Chuyển thời lượng "12:34" → giây
        parts = duration_text.split(":")
        if len(parts) == 2:
            total_seconds = int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            total_seconds = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        else:
            total_seconds = 30  # fallback

        # Giới hạn tối đa 2 phút để tránh test quá lâu
        watch_time = min(total_seconds, 120)
        print(f"🕒 Chờ xem video trong {watch_time} giây...")
        time.sleep(watch_time)

    except Exception as e:
        print("⚠️ Không lấy được thời lượng video, chờ mặc định 30 giây.")
        time.sleep(30)

    print("🏁 Hết thời gian xem video. Kết thúc test.")
    page.screenshot(path="youtube_video_end.png")
