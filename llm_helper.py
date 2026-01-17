from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline


model_name = "Qwen/Qwen2.5-Math-1.5B"
# cache_dir = "D:/huggingface_models"  # 自定义非C盘存储路径
device = "mps"  # M系列建议使用 "mps"，若可用则更快；默认用 CPU

# 加载模型与分词器
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True).to(device)
model.eval()

# 创建 pipeline（不使用 GPU 时 device=-1）
# explain_pipe = pipeline(
#     "text-generation",
#     model=model,
#     tokenizer=tokenizer,
#     device=-1
# )

def explain_expression(expr: str, result: str, log_steps: list[str]) -> str:
    """
    使用 LLM 给出表达式的计算解释，包含可信计算模块中记录的每一步日志
    """
    # 拼接日志内容
    steps_str = "\n".join([f"{i + 1}. {step}" for i, step in enumerate(log_steps)])

    # 构造中文提示词
    prompt = f"""
    你是一位精通数学的中文语言助手，掌握泰勒展开、误差控制等高精度计算方法。
    用户希望你解释下列表达式的计算过程：

    表达式：{expr}
    计算结果：{result}

    以下是可信计算中记录的**关键日志摘要**，省略了部分重复步骤：
    {steps_str}

    请你逐步解释该表达式是如何被准确计算的，包含：
    - 所使用的数学展开公式
    - 每一步误差如何控制
    - 各步骤目的与中间结果
    - 如何最终得出精确结果

    请使用通俗中文完整输出解释，不要重复题目。
    """

    # 编码 prompt 并生成
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=1024,
        do_sample=False,
        # do_sample=True,
        # temperature=0.7,
        # top_p=0.9,
        pad_token_id=tokenizer.eos_token_id
    )
    output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # 去掉模型可能重复输出的 prompt 内容，只保留答案部分
    if prompt.strip() in output_text:
        output_text = output_text.replace(prompt.strip(), "").strip()

    return output_text
