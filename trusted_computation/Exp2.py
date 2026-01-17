from fractions import Fraction
from decimal import Decimal
from .log_util import add_log

def get_fraction(a2):
    """
    将 a2 转换为简分数 n/m 的形式，并确保 m 是奇数。
    如果 m 是偶数，将其调整为最接近的奇数，同时调整 n。
    """
    # 将 a2 转换为简分数
    frac = Fraction(a2).limit_denominator()
    n = frac.numerator
    m = frac.denominator

    # 如果 m 是偶数，进行调整，确保 m 是奇数
    if m % 2 == 0:
        # 如果 m 是偶数，调整为奇数
        m += 1
        n = int(n * m / frac.denominator)  # 通过比例调整分子

    return n, m


def Exp2(a1, a2, epsilon):
    from .main import Main
    """
    计算 a1^a2，使用指数和对数的结合公式，满足误差限 epsilon。

    参数:
    a1 -- 输入值，可能是一个数值或表达式
    a2 -- 乘数
    epsilon -- 允许的误差限

    返回:
    近似值 y ≈ a1^a2，满足 |y - a1^a2| < epsilon
    """

    add_log(f"【Exp2】计算 {a1}^{a2}，误差限 ε = {epsilon}")

    a1_val = Decimal(Main(a1, epsilon))  # 正确获取 a1 的值
    a2_val = Decimal(Main(a2, epsilon))  # 同理处理 a2
    add_log(f"获取表达式值：a1 ≈ {a1_val}, a2 ≈ {a2_val}")

    # 特殊情况：如果 a1 = 0，直接返回 0
    if a1_val == 0:
        add_log(f"特例：a1 = 0 ⇒ 结果为 0")
        return Decimal(0)

    # 如果 a1 > 0，直接计算 exp(a2 * ln(a1))
    if a1_val > 0:
        add_log(f"a1 > 0，使用 exp(a2 × ln(a1))")
        return Main(('exp1', ('*', a2, ('ln', a1))), epsilon)

    # 如果 a1 < 0，根据 n 和 m 的奇偶性分别处理
    if a1_val < 0:
        # 计算 a2 的简分数表示 n/m
        n, m = get_fraction(a2)
        add_log(f"a1 < 0，a2 = {n}/{m}（化为最简分数）")

        if n % 2 == 0:  # 如果 n 是偶数
            add_log(f"n 为偶数 ⇒ 结果为实数 exp(a2 × ln(-a1))")
            return Main(('exp1', ('*', a2, ('ln', ('-', a1)))), epsilon)
        else:  # 如果 n 是奇数
            add_log(f"n 为奇数 ⇒ 结果为负数 -exp(a2 × ln(-a1))")
            return -Main(('exp1', ('*', a2, ('ln', ('-', a1)))), epsilon)