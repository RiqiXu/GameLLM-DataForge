import re

def evaluate_quality(text: str, data_type: str) -> dict:
    """
    基于启发式规则 (Rule-based) 评估清洗后的数据质量。
    返回一个字典，包含：
    - is_rejected: bool (是否被拒绝丢弃)
    - quality_score: float (质量分数 0.0 ~ 1.0)
    - rejected_reason: str (如果拒绝，拒绝的详细原因)
    """
    # 1. 空数据或解析失败的数据
    # 如果被 Cleaner 完全洗没，或者 AST 遇到语法错误返回了 None
    if not text or len(text.strip()) == 0:
        return {
            "is_rejected": True,
            "quality_score": 0.0,
            "rejected_reason": "Empty content or parsing failed"
        }

    text_length = len(text)

    # 2. 针对代码类数据 (Code) 的质量规则
    if data_type == "code":
        # 规则 2.1: 代码太短，缺乏逻辑学习价值
        if text_length < 20:
            return {
                "is_rejected": True, 
                "quality_score": 0.1, 
                "rejected_reason": "Code length too short (<20 chars)"
            }
        
        # 基础过关
        return {"is_rejected": False, "quality_score": 0.9, "rejected_reason": None}

    # 3. 针对自然语言文本 (general_text / game_text) 的质量规则
    else:
        # 规则 3.1: 文本太短，没有上下文信息
        if text_length < 10:
            return {
                "is_rejected": True, 
                "quality_score": 0.1, 
                "rejected_reason": "Text too short (<10 chars)"
            }

        # 规则 3.2: 正常字符（中英文字母、数字）占比过低，通常是乱码或颜文字堆砌
        # 使用正则找出所有正常字符
        alnum_count = len(re.findall(r'[a-zA-Z0-9\u4e00-\u9fa5]', text))
        alnum_ratio = alnum_count / text_length

        if alnum_ratio < 0.5:
            return {
                "is_rejected": True, 
                "quality_score": round(alnum_ratio, 2), 
                "rejected_reason": f"Low alphanumeric ratio ({alnum_ratio:.2f}) - suspected gibberish"
            }

        # 满分通过，正常字符比例越高，得分越高
        final_score = 0.8 + (0.2 * alnum_ratio)
        return {"is_rejected": False, "quality_score": round(final_score, 2), "rejected_reason": None}

# --- 本地快速测试代码 ---
if __name__ == "__main__":
    print("【测试 1：极短的废话文本】")
    res1 = evaluate_quality("你好", "game_text")
    print(res1)
    
    print("\n【测试 2：全是特殊符号的乱码文本】")
    res2 = evaluate_quality("！！！@@@￥￥￥真难打", "game_text")
    print(res2)
    
    print("\n【测试 3：优质的高质量游戏文本】")
    res3 = evaluate_quality("原神深渊 12 层上半，建议使用雷神国家队，循环非常流畅。", "game_text")
    print(res3)
    
    print("\n【测试 4：短于20个字符的无意义代码】")
    res4 = evaluate_quality("def a(): pass", "code")
    print(res4)