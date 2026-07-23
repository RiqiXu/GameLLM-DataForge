import json
import uuid

def generate_dummy_data():
    # 我们故意制造 4 条极具代表性的数据
    samples = [
        {
            "text": "原神启动！今天深渊真难打，#￥%……&*（乱码符）",
            "meta": {"source": "tieba", "language": "zh", "is_code": False}
        },
        {
            "text": "def calculate_damage(atk, def):\n    # TODO: 修复这个bug\n    return atk - def",
            "meta": {"source": "github_genshin_sim", "language": "python", "is_code": True}
        },
        {
            "text": "啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊", # 连续重复无意义字符
            "meta": {"source": "steam_reviews", "language": "zh", "is_code": False}
        },
        {
            "text": "<html><body>正常攻略文本</body><script>恶意代码</script></html>", # 混杂HTML标签
            "meta": {"source": "wiki", "language": "zh", "is_code": False}
        }
    ]

    # 将它们按照我们设计的 Schema 写入 JSONL 文件
    with open("data/raw/dummy_data.jsonl", "w", encoding="utf-8") as f:
        for sample in samples:
            # 补全我们在 Schema 里规定的必备字段
            sample["id"] = str(uuid.uuid4())
            sample["quality_score"] = None
            sample["rejected_reason"] = None
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")

    print("✅ 成功生成 4 条极具挑战性的 Mock 数据，已存入 data/raw/dummy_data.jsonl")

if __name__ == "__main__":
    generate_dummy_data()