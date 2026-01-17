from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN
import math
from .log_util import add_log, get_log_level

def ln(a, epsilon):
    from .main import Main
    math_e = Decimal(str(math.e))
    """
    计算 ln(a)，如果 a 是常数，则直接计算，如果是表达式则通过 main 进行处理。

    参数:
    a -- 输入值，可能是一个数值或表达式
    epsilon -- 允许的误差限

    返回:
    近似值 y ≈ ln(a)，满足 |y - ln(a)| < epsilon
    """
    # 处理ln(e)特例：直接返回1

    # 如果 a 是常数，直接计算 ln(a)
    if isinstance(a, (int, float, Decimal)):  # 判断是否为常数
        a = Decimal(a)  # 转为 Decimal 类型
        # add_log(f"【ln】ln({a}) a是常数")
        if abs(a - math_e) < epsilon:
            # add_log(f"特例：ln(e) ≈ 1")
            return Decimal(1)
        return ln1(a, epsilon)
    else:
        # 如果 a 是表达式，通过 Main 函数计算近似值
        # add_log(f"【ln】ln({a}) 是表达式")
        epsilon_prime = Decimal('0.1')  # 初始化 ε′ 为 0.1
        a_tilde = Decimal(Main(a, epsilon_prime))  # 计算满足误差要求的 a_tilde
        # add_log(f"初步估算 ã ≈ {a_tilde}（ε′ = {epsilon_prime}）")

        # 调整 ε′ 直到满足条件
        while abs(a_tilde) <= 2 * epsilon_prime or 2 * epsilon_prime > (abs(a_tilde) - epsilon_prime) * epsilon:
            epsilon_prime *= Decimal('0.1')  # 缩小 ε′
            a_tilde = Decimal(Main(a, epsilon_prime))  # 重新计算 a_tilde
            # add_log(f"调整 ε′ 为 {epsilon_prime}，ã 更新为 {a_tilde}")

        # 返回 ln(a_tilde)，误差精度为 ε/2
        # add_log(f"最终 ã ≈ {a_tilde}，使用 ln1 计算")
        return ln1(a_tilde, epsilon / 2)


def ln1(c, epsilon):
    # from .main import Main
    """
    计算自然对数 ln(c)，使用泰勒展开，满足误差限 epsilon。

    参数:
    c -- 输入值，可能是一个数值或表达式
    epsilon -- 允许的误差限

    返回:
    近似值 y ≈ ln(c)，满足 |y - ln(c)| < epsilon
    """
    c = Decimal(c)  # 将输入值转换为 Decimal 类型，以便进行高精度计算

    if c == 1:  # 如果 c = 1，返回 0
        # add_log("【ln1】ln(1) = 0")
        return Decimal(0)

    if c <= 0:
        raise ValueError(f"ln({c}) 未定义，ln(x),x必须为正数")

# ========== 日志（摘要级） ==========
    log_level = get_log_level()
    if log_level != "NONE":
        add_log(f"【ln】使用对称泰勒展开计算 ln({c})", level="SUMMARY")

# ========== 算法实现 ==========

    # 初始化 n 和项
    n = 1
    term = (2 * (c - 1)) / (c + 1)  # 第一项是 (2 * (c - 1)) / (c + 1)
    result = term  # 初始化结果为第一项
    add_log(f"【ln1】ln({c}) 使用泰勒展开，初始项: {term}")

    # 循环计算每一项，直到满足误差条件
    while 2 * abs(c - 1) ** (2 * n + 1) >= 4 * n * c * (c + 1) ** (2 * n - 1) * epsilon:  # 判断当前项是否满足精度要求
        n += 1
        current_term = (2 * (c - 1) ** (2 * n - 1)) / ((2 * n - 1) * (c + 1) ** (2 * n - 1))
        result += current_term  # 累加每一项
        # add_log(f"第 {n} 项: {current_term}，累计结果: {result}")

# ========== 日志：只记录项数 ==========
    if log_level == "SUMMARY":
        add_log(
            f"【ln】展开 {n} 项，满足 |最后一项| < ε/2，结果已收敛",
            level="SUMMARY"
        )

    return Decimal(result)