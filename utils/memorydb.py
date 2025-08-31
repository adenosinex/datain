import sqlite3
from typing import Optional

class InMemoryURLDB:
    def __init__(self,db="urlcontent.db"):
        # 创建内存数据库
        self.conn = sqlite3.connect(db, check_same_thread=False)
        # self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # 支持按列名访问
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """创建表：urls (url TEXT PRIMARY KEY, content TEXT)"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                url TEXT PRIMARY KEY,
                content TEXT
            )
        ''')
        self.conn.commit()

    def set_url(self, url: str) -> bool:
        """
        插入新 URL，content 初始为 NULL
        如果 URL 已存在，不更新 content
        """
        try:
            self.cursor.execute(
                "INSERT OR IGNORE INTO urls (url, content) VALUES (?, NULL)",
                (url,)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"❌ 插入 URL 失败: {e}")
            return False

    def complete_content(self, url: str, content: str) -> bool:
        """
        为指定 URL 补全 content
        如果 URL 不存在，会插入新记录
        """
        try:
            self.cursor.execute(
                "INSERT OR REPLACE INTO urls (url, content) VALUES (?, ?)",
                (url, content)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"❌ 更新 content 失败: {e}")
            return False

    def get_content(self, url: str) -> Optional[str]:
        """
        获取指定 URL 的 content
        返回字符串或 None（未找到或 content 为空）
        """
        self.cursor.execute(
            "SELECT content FROM urls WHERE url = ?", (url,)
        )
        row = self.cursor.fetchone()
        return row["content"] if row else None
    def get_url(self ) -> Optional[str]:
        """
        获取指定 URL 的 content
        返回字符串或 None（未找到或 content 为空）
        """
        self.cursor.execute(
            "SELECT url FROM urls where content is null"
        )
        row = self.cursor.fetchone()
        return row["url"] if row else None

    def url_exists(self, url: str) -> bool:
        """检查 URL 是否已存在"""
        self.cursor.execute("SELECT 1 FROM urls WHERE url = ? LIMIT 1", (url,))
        return self.cursor.fetchone() is not None

    def close(self):
        """关闭数据库连接"""
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == "__main__":
    # 使用上下文管理器（推荐）
    with InMemoryURLDB(r'utils\urlcontent.db') as db:
        # 1. 设置 URL
        db.set_url("https://example.com")
        db.set_url("https://httpbin.org")

        # 2. 补全 content
        db.complete_content("https://example.com", "<html>Example</html>")
        db.complete_content("https://httpbin.org", "JSON Test Response")

        # 3. 获取 content
        content = db.get_content("https://example.com")
        print("Content:", content)

        # 4. 检查 URL 是否存在
        print("Exists:", db.url_exists("https://example.com"))