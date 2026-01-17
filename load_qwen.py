import os
# os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "Qwen/Qwen2.5-Math-1.5B-Instruct"

print(f"准备下载/加载模型: {model_name}")

# 自动选择设备 (与 llm_helper.py 保持一致的逻辑)
device = "mps" if torch.backends.mps.is_available() else "cpu"
if torch.cuda.is_available():
    device = "cuda"
print(f"使用设备: {device}")

try:
    # 加载分词器
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

    # 加载模型
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        trust_remote_code=True,
        device_map=device  # 显式指定设备
    )

    print("\n✅ 模型加载成功！")
    print(f"模型已缓存至本地 (默认路径: ~/.cache/huggingface/hub)")
    print("现在可以运行 app.py 了。")

except Exception as e:
    print(f"\n❌ 模型加载失败: {e}")
    print("请检查网络连接，或尝试配置 HF_ENDPOINT 环境变量。")