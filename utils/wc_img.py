# pip install jieba wordcloud

import os
from pathlib import Path
import jieba
from wordcloud import WordCloud

# pip install jieba wordcloud  
class ChineseWordCloud:
    """
    中文词云生成器类
    支持：自动分词、去停用词、固定文字方向、后台可调用
    """
    def __init__(self, font_path: str = "msyh.ttc", stopwords_file: str = None):
        """
        初始化

        参数:
        - font_path: 中文字体路径
        - stopwords_file: 可选停用词文件路径，每行一个词
        """
        self.font_path = font_path
        # 默认停用词
        self.stopwords = set([
            "的", "了", "在", "是", "我", "有", "和", "也", "就", "不", "人", "都"
        ])
        # 加载外部停用词
        if stopwords_file:
            try:
                with open(stopwords_file, "r", encoding="utf-8") as f:
                    extra_words = [x.strip() for x in f.readlines()]
                    self.stopwords.update(extra_words)
            except Exception as e:
                print(f"加载停用词失败: {e}")

    def generate(self, text: str, output_file: str = "wordcloud.png", 
                 max_words: int = 200, width: int = 800, height: int = 600,
                 show: bool = False):
        """
        生成词云并保存图片

        参数:
        - text: 中文文本
        - output_file: 输出图片路径
        - max_words: 最大词数
        - width, height: 图片尺寸
        - show: 是否显示图片（matplotlib，可选）
        """
        # 分词并去停用词
        words = jieba.lcut(text)
        words = [w for w in words if w.strip() and w not in self.stopwords]
        segmented_text = " ".join(words)

        # 生成词云
        wc = WordCloud(
            font_path=self.font_path,
            width=width,
            height=height,
            background_color="white",
            max_words=max_words,
            prefer_horizontal=1.0  # 所有文字水平
        )
        wc.generate(segmented_text)
        wc.to_file(output_file)
        if show:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(width/100, height/100))
            plt.imshow(wc, interpolation="bilinear")
            plt.axis("off")
            plt.show()
        return output_file

# ------------------- 使用示例 -------------------

def get_allfiles(folder):
    files=[]
    for i in os.walk(folder):
        for j in i[2]:
            files.append(Path(i[0]).joinpath(j))
    return files

def factory_wc():
    wc_generator = ChineseWordCloud(
        font_path="msyh.ttc",
        stopwords_file=r"data\百度停用词表.txt"
    )
    def f(text):
        if len(text)<200 and os.path.isdir(text):
            text=' '.join([i.stem for i in get_allfiles(text)  ])
        return wc_generator.generate(text)
    return f

if __name__ == "__main__":
    # 初始化类
    wc=factory_wc()
    # 读取文本
    with open("a.txt", "r", encoding="utf-8") as f:
        text = f.read()
    
    # 生成词云
    wc(text, output_file="my_wordcloud.png", show=True)
