import os
# os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from decimal import Decimal, getcontext
from trusted_computation.input import parse_expression
from trusted_computation.main import Main, format_sig_digits
from trusted_computation.pi import get_pi
from trusted_computation.log_util import clear_log, get_log
from llm_helper import explain_expression
import traceback


def run_calculator():
    print("=== AI 可信计算器 (v1.2 Explainable) ===")

    while True:
        print("\n" + "=" * 50)
        user_input = input("请输入数学表达式 (q退出): ").replace("^", "**")
        if not user_input or user_input.lower() == 'q':
            break

        try:
            # 1. 获取精度设置
            sig_digits_str = input("请输入保留有效数字位数 (默认100): ")
            sig_digits = int(sig_digits_str.strip()) if sig_digits_str.strip() else 100

            # 设置极高的内部计算精度，确保最后保留的有效数字是准确的
            # ε (epsilon) 用于算法内部的误差控制
            ε = Decimal(10) ** (-1000)

            # Decimal 上下文精度要比目标有效数字大，这里设得非常大以防万一
            getcontext().prec = sig_digits + 1000

            print(f"--- 初始化: 目标精度 {sig_digits} 位，内部误差限 ε = 1E-1000 ---")

            # 2. 预热/缓存常数
            get_pi(ε)

            # 3. 解析表达式
            parsed_expr = parse_expression(user_input)
            print(f"解析结果: {parsed_expr}")

            # 4. 执行计算（关键修改）
            # === Step 1: 清空旧日志 ===
            clear_log()

            # === Step 2: 调用 Main，开启 explain 模式 ===
            # 这会自动记录 SUMMARY 级别的日志，而隐藏内部高精度逼近的 DETAIL 日志
            print("正在进行可信计算...")
            result = Main(parsed_expr, ε, mode="explain")

            # 5. 格式化结果
            sig_result = format_sig_digits(result, sig_digits)
            print("-" * 30)
            print(f"计算结果 (前50位): {str(result)[:50]}...")
            print(f"最终结果 ({sig_digits}位有效数字): \n{sig_result}")

            # 6. 获取日志并调用 LLM
            # 由于底层已经做了分级，这里直接获取的就是“摘要”
            log_steps = get_log()

            print(f"\n【计算过程追踪】共记录 {len(log_steps)} 个关键步骤")
            # 打印前几步示例
            if len(log_steps) > 5:
                for i in range(3): print(f"  {i + 1}. {log_steps[i]}")
                print(f"  ... (省略 {len(log_steps) - 4} 步) ...")
                print(f"  {len(log_steps)}. {log_steps[-1]}")
            else:
                for i, step in enumerate(log_steps):
                    print(f"  {i + 1}. {step}")

            # 调用 LLM 生成自然语言解释
            print("\n正在生成 AI 解释报告...")
            explanation = explain_expression(user_input, sig_result, log_steps)
            print("\n" + "*" * 20 + " AI 数学解释 " + "*" * 20)
            print(explanation)
            print("*" * 55)

        except Exception as e:
            print(f"发生错误: {e}")
            traceback.print_exc()


if __name__ == "__main__":
    run_calculator()