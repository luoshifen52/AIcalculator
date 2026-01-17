from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# 1. 模型名称
model_name = "Qwen/Qwen2.5-Math-1.5B-Instruct"

# 2. 【核心修复】强制使用 CPU，避开 MacOS MPS 的 4GB 显存分配 Bug
# 虽然 MPS (GPU) 理论上更快，但对于 1.5B 这种小模型，
# M1/M2/M3 芯片的 CPU 性能绰绰有余，且稳定性 100%。
device = "cpu"
# 如果检测到是 NVIDIA 显卡（Windows/Linux），依然使用 cuda
if torch.cuda.is_available():
    device = "cuda"

print(f"正在加载模型 {model_name} 到 {device} (强制 CPU 以保证 Mac 稳定性)...")

try:
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

    # 【修改】CPU 模式下建议使用 float32 (默认)，兼容性最好
    # 移除 torch_dtype=torch.float16，防止 CPU 不支持某些半精度算子
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        trust_remote_code=True,
        low_cpu_mem_usage=True  # 优化加载过程内存
    ).to(device)

    model.eval()
    print("模型加载完成。")
except Exception as e:
    print(f"模型加载失败: {e}")
    print("请检查网络或确认 huggingface 访问权限。")


def explain_expression(expr: str, result: str, log_steps: list[str]) -> str:
    """
    使用 LLM 根据可信计算日志生成解释
    """
    # 日志截断
    max_steps = 60
    if len(log_steps) > max_steps:
        display_steps = log_steps[:25] + [f"...(中间省略 {len(log_steps) - 50} 步)..."] + log_steps[-25:]
    else:
        display_steps = log_steps

    steps_str = "\n".join([f"{i + 1}. {step}" for i, step in enumerate(display_steps)])

    # 构造 Prompt
    prompt_content = f"""
    你是一个数学与算法专家。用户通过“可信计算器”计算了表达式 {expr}，得到了高精度结果。
    请根据【执行日志】解释计算过程。

    【用户表达式】
    {expr}

    【计算结果】
    {result}

    【执行日志 (Key Execution Trace)】
    {steps_str}

    【任务要求】
    1. 忽略日志中的技术噪声，用**通俗流畅的中文**解释核心步骤。
    2. 注意：日志中可能包含为了确定精度而进行的“粗略估算”步骤，以及随后的“精确计算”步骤，请将它们归纳为“先估算...再精确计算...”。
    3. 重点解释算法策略（如：为何使用泰勒展开、如何控制误差限 ε）。
    4. **严禁编造**不存在的人名（如Jack）或无关内容。
    5. 不要重复输出大段相同的文字。
    """

    messages = [
        {"role": "system", "content": "你是一位严谨、逻辑清晰的数学与计算机科学助教。请用中文回答。"},
        {"role": "user", "content": prompt_content}
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer([text], return_tensors="pt").to(device)

    # 生成参数优化
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=800,
            do_sample=True,
            temperature=0.2,  # 保持低温采样
            top_p=0.85,
            repetition_penalty=1.1,
        )

    input_len = inputs.input_ids.shape[1]
    generated_ids = outputs[0][input_len:]
    response = tokenizer.decode(generated_ids, skip_special_tokens=True)

    return response.strip()