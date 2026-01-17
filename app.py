import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from decimal import Decimal, getcontext
from trusted_computation.main import Main, parse_expression, get_pi, format_sig_digits
from trusted_computation.log_util import clear_log, get_log, summarize_log_steps
from llm_helper import explain_expression  # 加入解释函数
from trusted_computation.pi import reset_pi_cache

while True:
    user_input = input("请输入数学表达式: ").replace("^", "**")  # 先替换 ^ 为 **
    if not user_input:
        break

    try:
        sig_digits = input("请输入保留有效数字位数(默认100位): ")
        sig_digits = int(sig_digits.strip()) if sig_digits.strip() else 100
        # ε = Decimal(10) ** (-sig_digits)  # ε 仍用于误差控制
        ε = Decimal(10) ** (-1000)  # ε 仍用于误差控制 !!!!!!!!
        print(f"计算精度: ε = {ε}")
        getcontext().prec = sig_digits + 1000  # Decimal 内部计算精度 !!!!!!!!内部计算精度

        get_pi(ε)  # 缓存pi值，避免死循环

        # === 清空日志 ===
        clear_log()

        parsed_expr = parse_expression(user_input)
        print(f"转换后的数学操作树: {parsed_expr}")
        result = Main(parsed_expr, ε)

        sig_result = format_sig_digits(result, sig_digits)
        print(f"计算结果: {result}")
        print(f"计算结果（{sig_digits}位有效数字）: {sig_result}")
        print(f"计算精度: ε = {ε}")

        # === 获取原始日志并摘要 ===
        log_steps = get_log()
        summary_steps = summarize_log_steps(log_steps, max_lines=120)

        print("\n【计算过程日志（摘要 ）")
        for step in summary_steps:
            print("→", step)

        # === 调用 LLM 获取解释（传入日志摘要） ===
        explanation = explain_expression(user_input, sig_result, summary_steps)
        print("\n【计算过程解释】\n")
        print(explanation)

    except ValueError as e:
        print(f"错误: {e}")

# expr = "e^(pi*(163^0.5))-262537412640768744"
# sig_digits = 100
# ε = Decimal(10) ** (-1000)
#
# parsed = parse_expression(expr)
# print("转换后的表达式树:", parsed)
# result = Main(parsed, ε)
#
# print(f"计算结果（{sig_digits}位有效数字）: {result}")