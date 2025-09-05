import json
import os
from typing import Dict, List, Optional

class BookmarkManager:
    def __init__(self, bookmarks_file: str = "data/bookmarks.json"):
        """
        初始化书签管理器
        
        Args:
            bookmarks_file: 书签数据文件路径
        """
        self.bookmarks_file = bookmarks_file
        self._bookmarks_data = None 
    
    def load_bookmarks(self) -> Dict:
        """
        加载书签数据
        
        Returns:
            书签数据字典
        """
        if self._bookmarks_data is None:
            try:
                if os.path.exists(self.bookmarks_file):
                    with open(self.bookmarks_file, 'r', encoding='utf-8') as f:
                        self._bookmarks_data = json.load(f)
                else:
                    # 如果文件不存在，返回默认数据
                    self._bookmarks_data = self._get_default_bookmarks()
            except Exception as e:
                print(f"加载书签数据失败: {e}")
                self._bookmarks_data = self._get_default_bookmarks()
        
        return self._bookmarks_data
    
    def get_all_categories(self) -> List[Dict]:
        """
        获取所有书签分类
        
        Returns:
            分类列表
        """
        data = self.load_bookmarks()
        return data.get('categories', [])
    
    def get_category_by_id(self, category_id: str) -> Optional[Dict]:
        """
        根据ID获取分类
        
        Args:
            category_id: 分类ID
            
        Returns:
            分类数据，如果不存在返回None
        """
        categories = self.get_all_categories()
        for category in categories:
            if category.get('id') == category_id:
                return category
        return None
    
    def get_all_bookmarks(self) -> List[Dict]:
        """
        获取所有书签（扁平化）
        
        Returns:
            所有书签列表
        """
        categories = self.get_all_categories()
        all_bookmarks = []
        
        for category in categories:
            bookmarks = category.get('bookmarks', [])
            for bookmark in bookmarks:
                bookmark_with_category = bookmark.copy()
                bookmark_with_category['category'] = category.get('name')
                bookmark_with_category['category_id'] = category.get('id')
                bookmark_with_category['category_icon'] = category.get('icon')
                all_bookmarks.append(bookmark_with_category)
        
        return all_bookmarks
    
    def search_bookmarks(self, query: str) -> List[Dict]:
        """
        搜索书签
        
        Args:
            query: 搜索关键词
            
        Returns:
            匹配的书签列表
        """
        all_bookmarks = self.get_all_bookmarks()
        query = query.lower()
        
        results = []
        for bookmark in all_bookmarks:
            title = bookmark.get('title', '').lower()
            description = bookmark.get('description', '').lower()
            category = bookmark.get('category', '').lower()
            
            if (query in title or 
                query in description or 
                query in category):
                results.append(bookmark)
        
        return results
    
    def add_bookmark(self, category_id: str, bookmark: Dict) -> bool:
        """
        添加书签
        
        Args:
            category_id: 分类ID
            bookmark: 书签数据
            
        Returns:
            是否添加成功
        """
        data = self.load_bookmarks()
        categories = data.get('categories', [])
        
        for category in categories:
            if category.get('id') == category_id:
                if 'bookmarks' not in category:
                    category['bookmarks'] = []
                category['bookmarks'].append(bookmark)
                return self._save_bookmarks(data)
        
        return False
    
    def remove_bookmark(self, category_id: str, bookmark_title: str) -> bool:
        """
        删除书签
        
        Args:
            category_id: 分类ID
            bookmark_title: 书签标题
            
        Returns:
            是否删除成功
        """
        data = self.load_bookmarks()
        categories = data.get('categories', [])
        
        for category in categories:
            if category.get('id') == category_id:
                bookmarks = category.get('bookmarks', [])
                for i, bookmark in enumerate(bookmarks):
                    if bookmark.get('title') == bookmark_title:
                        del bookmarks[i]
                        return self._save_bookmarks(data)
        
        return False
    
    def _save_bookmarks(self, data: Dict) -> bool:
        """
        保存书签数据到文件
        
        Args:
            data: 书签数据
            
        Returns:
            是否保存成功
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.bookmarks_file), exist_ok=True)
            
            with open(self.bookmarks_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # 更新内存中的数据
            self._bookmarks_data = data
            return True
        except Exception as e:
            print(f"保存书签数据失败: {e}")
            return False
    
    def _get_default_bookmarks(self) -> Dict:
        """
        获取默认书签数据
        
        Returns:
            默认书签数据
        """
        return {
            "categories": [
                {
                    "id": "news",
                    "name": "新闻与时事",
                    "icon": "📰",
                    "description": "全球新闻与时事资讯",
                    "bookmarks": [
                        {
                            "title": "BBC News",
                            "url": "https://www.bbc.com/news",
                            "icon": "🌍",
                            "description": "提供全球范围的新闻报道"
                        }
                    ]
                }
            ]
        }
    
    def reload_bookmarks(self):
        """
        重新加载书签数据
        """
        self._bookmarks_data = None
        return self.load_bookmarks()

# 创建全局实例
bookmark_manager = BookmarkManager()
