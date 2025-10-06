import os
import hashlib
import shutil
import sqlite3
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


from typing import Iterator

from tqdm import tqdm

def iter_files(folder: str|Path) -> Iterator[str]:
    """生成器模式高效遍历"""
    try:
        with os.scandir(folder) as entries:
            for entry in entries:
                try:
                    if entry.is_file():
                        yield entry.path
                    elif entry.is_dir():
                        yield from iter_files(entry.path)
                except OSError as e:
                    print(f"跳过异常条目 {entry.path}: {e}")
    except PermissionError:
        print(f"无权限访问目录: {folder}")

class FolderIndex:
    def __init__(self, folder, db_file="file_index.db", block_size=1024*1024):
        """
        :param folder: 目标文件夹
        :param db_file: 索引数据库文件
        :param block_size: 参与哈希的文件块大小（默认 1MB）
        """
        self.folder = Path(folder)
        self.folder.mkdir(parents=True, exist_ok=True)
        self.db_file = self.folder / db_file
        self.block_size = block_size
        self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
        self._init_db()

    def _init_db(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS files (
                hash TEXT PRIMARY KEY,
                path TEXT
            )
        """)
        self.conn.commit()

    def _partial_hash(self, path):
        """计算文件部分哈希（头 + 尾）"""
        hasher = hashlib.md5()
        size = os.path.getsize(path)

        with open(path, "rb") as f:
            # 读头
            head = f.read(self.block_size)
            hasher.update(head)

            if size > self.block_size:
                # 读尾
                f.seek(-self.block_size, os.SEEK_END)
                tail = f.read(self.block_size)
                hasher.update(tail)

        return hasher.hexdigest()

    def _is_duplicate(self, fhash):
        cur = self.conn.cursor()
        cur.execute("SELECT 1 FROM files WHERE hash=?", (fhash,))
        return cur.fetchone() is not None

    def _add_to_index(self, fhash, path):
        cur = self.conn.cursor()
        cur.execute("INSERT OR REPLACE INTO files (hash, path) VALUES (?, ?)", (fhash, path))
        self.conn.commit()

    def index_all(self, workers=4):
        """
        索引整个文件夹
        :param workers: 并行线程数（机械盘建议 2-4，固态可设高一些）
        """
        print(f"开始索引: {self.folder}")
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {}
            allFiles=iter_files(self.folder)
            for pt in allFiles:
                if os.path.isfile(pt) and not self.db_file.samefile(pt):
                    futures[executor.submit(self._partial_hash, pt)] = pt

            for future in tqdm(as_completed(futures), total=len(futures), desc="索引进度"):
                path = futures[future]
                
                try:
                    fhash = future.result()
                    self._add_to_index(fhash, path)
                except Exception as e:
                    print(f"索引失败 {path}: {e}")

    def exists(self, filepath):
        """判断文件是否已存在于文件夹"""
        fhash = self._partial_hash(filepath)
        return self._is_duplicate(fhash)

    def add_file(self, filepath, move=True):
        """添加新文件到文件夹，并更新索引"""
        fhash = self._partial_hash(filepath)
        if self._is_duplicate(fhash):
            print(f"文件已存在: {filepath}")
            return False

        dst_path = self.folder / Path(filepath).name
        if move:
            shutil.move(filepath, dst_path)
        else:
            shutil.copy2(filepath, dst_path)

        self._add_to_index(fhash, str(dst_path))
        print(f"添加并索引: {dst_path}")
        return True

    def close(self):
        self.conn.close()

def temp1():
    folder = FolderIndex(r"C:\Users\xin\Downloads\ProjectEye")
    # 第一次建立索引
    folder.index_all(workers=4)
    t=r'C:\Users\xin\Downloads\ProjectEye\ProjectEyeBug.exe'
    # 判断文件是否已存在
    print(folder.exists(t))

    # 添加新文件（默认移动，也可改成复制）
    # folder.add_file("新文件.mp4")

    # 关闭数据库
    folder.close()

    

if __name__ == "__main__":
        # 初始化（SSD 推荐 workers=8+，机械盘 workers=2-4）
    folder = FolderIndex(r"C:\Users\xin\Downloads\ProjectEye")

    # 第一次建立索引
    folder.index_all(workers=4)
    t=r'C:\Users\xin\Downloads\ProjectEye\ProjectEyeBug.exe'
    # 判断文件是否已存在
    print(folder.exists(t))

    # 添加新文件（默认移动，也可改成复制）
    # folder.add_file("新文件.mp4")

    # 关闭数据库
    folder.close()

