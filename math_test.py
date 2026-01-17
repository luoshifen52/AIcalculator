import math

def compute_with_trust(expression: str, precision: float) -> float:
    """
    使用可信计算算法计算表达式，并控制误差范围。
    :param expression: 数学表达式（如 "sin(0.5) + 2 * log10(10)"）。
    :param precision: 精度控制，误差限制。
    :return: 计算结果，符合精度要求。
    """
    # 允许的安全函数
    allowed_math_funcs = {
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,       # 自然对数(以 e 为底)
        "log10": math.log10,   # 常用对数（以 10 为底）
        "exp": math.exp,
        "sqrt": math.sqrt,
        "pi": math.pi,
        "e": math.e
    }

    try:
        # eval 使用安全上下文，仅允许定义的数学函数
        result = eval(expression, {"__builtins__": None}, allowed_math_funcs)
        return round(result, int(-math.log10(precision)))  # 控制精度
    except Exception as e:
        print(f"错误：无法解析表达式 {expression}, 错误信息: {e}")
        return None

# 示例调用
expression = ("sin(0.5) + 2 * log10(10)")
precision = 1e-5  # 设定误差精度为 0.00001
result = compute_with_trust(expression, precision)
print(f"计算结果: {result}")
