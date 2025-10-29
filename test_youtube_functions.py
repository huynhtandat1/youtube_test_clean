
from playwright.sync_api import Page, expect
from re import search
import pytest

@pytest.fixture(scope="function", autouse=True)
def slow_load(page: Page):
    page.set_default_timeout(20000)
    page.set_default_navigation_timeout(20000)

def accept_cookies(page: Page):
    """Nếu có nút 'Accept all' thì bấm để tránh bị chặn."""
    accept = page.locator("button:has-text('Accept all')")
    if accept.is_visible():
        accept.click()

# 1️⃣ Mở trang chủ YouTube
def test_open_youtube(page: Page):
    page.goto("https://www.youtube.com")
    page.wait_for_load_state("networkidle")
    accept_cookies(page)
    page.wait_for_selector('input#search, input[name="search_query"]', timeout=10000)
    search_box = page.locator('input#search, input[name="search_query"]').first
    expect(search_box).to_be_visible()

# 2️⃣ Tìm kiếm video
def test_search_video(page: Page):
    page.goto("https://www.youtube.com")
    accept_cookies(page)
    page.locator("input#search").fill("music video")
    page.locator("button#search-icon-legacy").click()
    expect(page).to_have_url(lambda url: "results" in url)
    expect(page.locator("ytd-watch-metadata #description").first).to_be_visible()
    expect(page.locator("h1.title").first).to_be_visible()


# 3️⃣ Mở video đầu tiên
def test_play_first_video(page: Page):
    page.goto("https://www.youtube.com/results?search_query=music+video")
    accept_cookies(page)
    page.locator("ytd-video-renderer").first.click()
    main_video = page.locator("#movie_player video")
    expect(main_video).to_be_visible()

# 4️⃣ Dừng / phát video
def test_pause_and_play(page: Page):
    page.goto("https://www.youtube.com/results?search_query=music+video")
    accept_cookies(page)
    page.locator("ytd-video-renderer").first.click()
    video = page.locator("#movie_player video")
    expect(video).to_be_visible()
    page.keyboard.press("k")  # Pause
    page.wait_for_timeout(2000)
    page.keyboard.press("k")  # Play
    page.wait_for_timeout(2000)

# 5️⃣ Bật / tắt full-screen
def test_fullscreen(page: Page):
    page.goto("https://www.youtube.com/results?search_query=music+video")
    accept_cookies(page)
    page.locator("ytd-video-renderer").first.click()
    video = page.locator("#movie_player video")
    expect(video).to_be_visible()
    page.keyboard.press("f")  # Fullscreen
    page.wait_for_timeout(2000)
    page.keyboard.press("f")  # Exit
    page.wait_for_timeout(2000)

# 6️⃣ Mở phần mô tả video
def test_open_description(page: Page):
    page.goto("https://www.youtube.com/results?search_query=music+video")
    accept_cookies(page)
    page.locator("ytd-video-renderer").first.click()
    show_more = page.locator("tp-yt-paper-button#expand")
    if show_more.is_visible():
        show_more.click()
    page.mouse.wheel(0, 8000)  # Cuộn sâu hơn
    page.wait_for_timeout(5000)    
    expect(page.locator("ytd-watch-metadata #description")).to_be_visible()

# 7️⃣ Kiểm tra bình luận
def test_check_comments(page: Page):
    page.goto("https://www.youtube.com/results?search_query=music+video")
    accept_cookies(page)
    page.locator("ytd-video-renderer").first.click()
    # Cuộn xuống để hiển thị bình luận
    page.wait_for_timeout(2000)
    page.mouse.wheel(0, 4000)
    page.wait_for_timeout(3000)
    comments = page.locator("ytd-comment-thread-renderer").first
    expect(comments).to_be_visible()

# Thêm một số bài kiểm tra nữa
def test_search_suggestions(page: Page):
    """Gõ một phần từ khóa và kiểm tra gợi ý tìm kiếm xuất hiện."""
    page.goto("https://www.youtube.com")
    accept_cookies(page)
    search = page.locator("input#search")
    search.fill("playwright")
    page.wait_for_timeout(2000)
    expect(page.locator("ytd-searchbox-suggestions, ytd-searchbox-suggestion").first).to_be_visible()

    # Đợi gợi ý hiện lên
    suggestions = page.locator("ytd-searchbox-suggestions, ytd-searchbox-suggestion")
    expect(suggestions.first).to_be_visible()

def test_related_videos_visible(page: Page):
    """Mở video đầu tiên và kiểm tra các video liên quan hiển thị ở sidebar."""
    page.goto("https://www.youtube.com/results?search_query=music+video")
    accept_cookies(page)
    page.locator("ytd-video-renderer").first.click()
    # Các video liên quan thường là compact renderers trong sidebar
    related = page.locator("ytd-compact-video-renderer, ytd-compact-autoplay-renderer")
    expect(related.first).to_be_visible()

def test_video_title_and_channel(page: Page):
    """Mở video và kiểm tra tiêu đề và tên kênh hiển thị."""
    page.goto("https://www.youtube.com/results?search_query=music+video")
    accept_cookies(page)
    page.locator("ytd-video-renderer").first.click()
    # Tiêu đề và tên kênh
    title = page.locator("h1.title yt-formatted-string, h1.title")
    channel = page.locator("ytd-channel-name a, #owner-name a")
    expect(title).to_be_visible()
    expect(channel).to_be_visible()

def test_subscribe_button_present(page: Page):
    """Kiểm tra nút Subscribe xuất hiện trên trang xem video (không cần bấm)."""
    page.goto("https://www.youtube.com/results?search_query=music+video")
    accept_cookies(page)
    page.locator("ytd-video-renderer").first.click()
    subscribe = page.locator("ytd-subscribe-button-renderer, tp-yt-paper-button#subscribe-button")
    expect(subscribe.first).to_be_visible()

def test_click_play_pause_first_video(page: Page):
    """Click vào video đầu tiên, phát và dừng video."""
    page.goto("https://www.youtube.com")
    accept_cookies(page)
    
    # Tìm kiếm video
    page.locator("input#search").fill("music video")
    page.locator("button#search-icon-legacy").click()
    
    # Click vào video đầu tiên
    page.locator("ytd-video-renderer").first.click()
    video = page.locator("#movie_player video")
    expect(video).to_be_visible()
    
    # Đợi video load
    page.wait_for_timeout(2000)
    
    # Click vào video để phát
    page.locator("#movie_player").click()
    page.wait_for_timeout(3000)  # Đợi video phát 3 giây
    
    # Click lần nữa để dừng
    page.locator("#movie_player").click()
    page.wait_for_timeout(1000)  # Đợi để xác nhận video đã dừng
