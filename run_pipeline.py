import json
import os
from src.text_cleaner import clean_text
from src.code_cleaner import clean_python_code
from src.quality_scorer import evaluate_quality

def generate_report(stats: dict, report_path: str):
    """
    自动生成 Markdown 格式的数据质量报告
    """
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# GameLLM-DataForge 自动数据质量报告\n\n")
        f.write(f"- **总处理数据量**: {stats['total']}\n")
        f.write(f"- **验收通过 (Processed)**: {stats['accepted']} 条\n")
        f.write(f"- **拒绝剔除 (Rejected)**: {stats['rejected']} 条\n\n")
        
        f.write("### 拒绝原因分布 (Rejection Reasons)\n")
        for reason, count in stats['rejection_reasons'].items():
            f.write(f"- `{reason}`: {count} 条\n")
            
    print(f"\n 质检报告已自动生成至: {report_path}")

def run_pipeline():
    print("[GameLLM-DataForge] 数据处理流水线启动...")
    
    # 1. 定义输入和输出路径
    raw_file = "data/raw/dummy_data.jsonl"
    processed_file = "data/processed/clean_data.jsonl"
    rejected_file = "data/rejected/rejected_data.jsonl"
    report_file = "reports/quality_report_dummy.md"

    # 确保输出文件夹存在
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("data/rejected", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    # 2. 初始化统计指标 (Telemetry)
    stats = {
        "total": 0,
        "accepted": 0,
        "rejected": 0,
        "rejection_reasons": {}
    }

    # 3. 逐行读取与处理 (Streaming 流式处理，防内存溢出)
    with open(raw_file, "r", encoding="utf-8") as f_in, \
         open(processed_file, "w", encoding="utf-8") as f_pass, \
         open(rejected_file, "w", encoding="utf-8") as f_fail:
         
        for line in f_in:
            if not line.strip():
                continue
                
            data = json.loads(line)
            stats["total"] += 1
            
            original_text = data.get("text", "")
            meta = data.get("meta", {})
            is_code = meta.get("is_code", False)
            data_type = "code" if is_code else "game_text"

            # 步骤 A: 路由清洗 (Data Cleaning)
            if is_code:
                cleaned_text = clean_python_code(original_text)
            else:
                cleaned_text = clean_text(original_text)

            # 步骤 B: 质量打分 (Quality Scoring)
            quality_result = evaluate_quality(cleaned_text, data_type)
            
            # 步骤 C: 结果组装与输出 (Data Routing)
            # 将原始的脏文本替换为干净的文本
            data["text"] = cleaned_text if cleaned_text else ""
            # 附加上我们 Schema 规定的输出字段
            data["processing_result"] = quality_result
            
            # 转回 JSON 字符串
            out_line = json.dumps(data, ensure_ascii=False) + "\n"
            
            if quality_result["is_rejected"]:
                f_fail.write(out_line)
                stats["rejected"] += 1
                reason = quality_result["rejected_reason"]
                stats["rejection_reasons"][reason] = stats["rejection_reasons"].get(reason, 0) + 1
            else:
                f_pass.write(out_line)
                stats["accepted"] += 1

    # 4. 触发报告生成
    generate_report(stats, report_file)
    print("恭喜！流水线端到端运行完毕！")

if __name__ == "__main__":
    run_pipeline()