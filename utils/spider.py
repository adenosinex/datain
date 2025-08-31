import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import traceback


class StealthBrowser:
    def __init__(self, headless=True):
        self.playwright = sync_playwright().start()
        # 创建浏览器
        self.browser = self.playwright.chromium.launch(
            headless=headless,
            args=["--disable-blink-features=AutomationControlled"]
        )

        # 创建 Context（在这里设置 UA、语言等）
        self.context = self.browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/116.0.0.0 Safari/537.36"
            ),
            locale="zh-CN",
            viewport={"width": 1920, "height": 1080},
            java_script_enabled=True
        )

        # 创建 Page
        self.page = self.context.new_page()

    def get_html(self, url):
        """获取网页 HTML 源码"""
        try:
            self.page.goto(url, timeout=5000)  # 20s 超时
            self.page.wait_for_load_state("networkidle")  # 等待页面加载完成
            return self.page.content()
        except Exception as e:
            print("❌ 获取 HTML 失败:", e)
            traceback.print_exc()
            return self.page.content()

    def get_text(self, url):
        """获取网页纯文本"""
        html = self.get_html(url)
        if html:
            soup = BeautifulSoup(html, "html.parser")
            return soup.get_text(separator="\n", strip=True)
        return None

    def quit(self):
        """关闭浏览器"""
        try:
            self.context.close()
            self.browser.close()
            self.playwright.stop()
        except Exception as e:
            print("❌ 关闭浏览器失败:", e)


# =======================
# 使用示例
# =======================
if __name__ == "__main__":
    bot = StealthBrowser(headless=True)

    url = "https://zhuanlan.zhihu.com/p/15865355450"
    from   memorydb import InMemoryURLDB
    db= InMemoryURLDB(r'utils\urlcontent.db')
    while True:
        url=db.get_url()
        if url:
            text = bot.get_text(url)
            if text:
                print("纯文本预览:", len(text), "...\n")

            db.complete_content(url, text)
        else:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"没有待处理的 URL，等待5秒...")
        time.sleep(0.5)
    bot.quit()
