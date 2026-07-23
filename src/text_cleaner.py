import re

def clean_text(text: str) -> str:
    """
    清洗通用文本和游戏文本流水线。
    包含：HTML标签过滤、连续冗余字符压缩、空白符规范化。
    """
    # 如果传入的文本是空的，直接返回空字符串
    if not text or not isinstance(text, str):
        return ""

    cleaned = text

    # 工序 1：剔除 HTML 标签 (例如 <html><body>内容</body> -> 内容)
    # 匹配以 < 开头，以 > 结尾的任意非尖括号内容，替换为空
    cleaned = re.sub(r'<[^>]+>', '', cleaned)

    # 工序 2：压缩连续重复的字符 (例如 "啊啊啊啊啊啊" -> "啊啊啊")
    # (.) 捕获任意字符，\1{4,} 表示这个字符连续重复出现至少 4 次
    # r'\1\1\1' 表示将这些超长重复替换为仅保留 3 次
    cleaned = re.sub(r'(.)\1{4,}', r'\1\1\1', cleaned)

    # 工序 3：规范化连续空白符 (例如连续的多个空格、换行、Tab符)
    # \s+ 匹配一个或多个空白字符，统一替换为单个空格
    cleaned = re.sub(r'\s+', ' ', cleaned)

    # 工序 4：去除文本首尾残留的空格
    cleaned = cleaned.strip()

    return cleaned

# --- 本地快速测试代码 ---
if __name__ == "__main__":
    # 我们构造一段包含 HTML、极其夸张的重复字符和多余空格的“极度脏数据”
    dirty_sample = """
    <html><body>
        原神启动！！！今天深渊真难打，啊啊啊啊啊啊啊啊啊啊！      
        <script>alert('恶意代码')</script>
    </body></html>
    """
    
    print("【原始脏数据】:")
    print(dirty_sample)
    print("-" * 40)
    print("【清洗后数据】:")
    print(clean_text(dirty_sample))